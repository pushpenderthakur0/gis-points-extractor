 
import arcpy
import csv
import os


class Toolbox(object):
    def __init__(self):
        self.label = "Points-in-Polygon Export"
        self.alias = "points_in_polygon_export"
        self.tools = [Pointcsv]


class Pointcsv(object):
    def __init__(self):
        self.label = "Point to CSV"
        self.description = (
            "Select points that fall within/intersect polygons filtered by a name field, "
            "and export their attributes to a CSV file."
        )
        self.canRunInBackground = True

    def getParameterInfo(self):
        points_fc = arcpy.Parameter(
            displayName="Points layer",
            name="points_fc",
            datatype="GPFeatureRecordSetLayer",
            parameterType="Required",
            direction="Input",
        )
        try:
            points_fc.schema = r"""
            {"geometryType": "esriGeometryPoint", "fields": [{"name": "OBJECTID", "type": "esriFieldTypeOID"}]}
            """.strip()
        except Exception:
            pass

        polygons_fc = arcpy.Parameter(
            displayName="Polygons layer",
            name="polygons_fc",
            datatype="GPFeatureRecordSetLayer",
            parameterType="Required",
            direction="Input",
        )
        try:
            polygons_fc.schema = r"""
            {"geometryType": "esriGeometryPolygon", "fields": [{"name": "OBJECTID", "type": "esriFieldTypeOID"}]}
            """.strip()
        except Exception:
            pass

        name_field = arcpy.Parameter(
            displayName="Name field (in polygons)",
            name="name_field",
            datatype="GPString",
            parameterType="Optional",
            direction="Input",
        )
        # Web AppBuilder does not support the Field parameter type. Use GPString instead.
        # Do not set a filter here so clients can type freely; we'll try to populate a dropdown in updateParameters when possible.

        name_value = arcpy.Parameter(
            displayName="Name value",
            name="name_value",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )

        predicate = arcpy.Parameter(
            displayName="Spatial predicate",
            name="predicate",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
        )
        predicate.filter.type = "ValueList"
        predicate.filter.list = ["WITHIN", "INTERSECT"]
        predicate.value = "WITHIN"

        case_sensitive = arcpy.Parameter(
            displayName="Case-sensitive name match",
            name="case_sensitive",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input",
        )
        case_sensitive.value = False

        output_csv = arcpy.Parameter(
            displayName="Output CSV",
            name="output_csv",
            datatype="DEFile",
            parameterType="Derived",
            direction="Output",
        )

        return [points_fc, polygons_fc, name_field, name_value, predicate, case_sensitive, output_csv]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        # Suggest a likely default (e.g., NAME, DISTRICT) if no value provided.
        try:
            polygons_fc_text = parameters[1].valueAsText if parameters[1].valueAsText else None
            name_field_param = parameters[2]
            if polygons_fc_text and name_field_param is not None:
                fields = [
                    f.name
                    for f in arcpy.ListFields(polygons_fc_text)
                    if f.type not in ("Geometry", "OID", "GlobalID")
                ]
                # If user hasn't provided a value, try to auto-fill a likely field name
                if fields and not name_field_param.value:
                    common_names_ordered = [
                        "NAME", "Name", "name",
                        "DIST_NAME", "DISTRICT", "District", "district",
                        "ADM1_EN", "ADM2_EN", "STATE", "STATE_NAME",
                        "GN_NAME", "GEO_NAME", "LABEL", "LABEL_NAME",
                    ]
                    for candidate in common_names_ordered:
                        if candidate in fields:
                            try:
                                name_field_param.value = candidate
                            except Exception:
                                pass
                            break
        except Exception:
            pass
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        points_fc = parameters[0].valueAsText
        polygons_fc = parameters[1].valueAsText
        name_field = parameters[2].valueAsText
        name_value = parameters[3].valueAsText
        predicate = parameters[4].valueAsText
        case_sensitive = bool(parameters[5].value)
 

        arcpy.AddMessage("Making feature layers...")
        arcpy.management.MakeFeatureLayer(points_fc, "points_lyr")
        arcpy.management.MakeFeatureLayer(polygons_fc, "polygons_lyr")

        # If name_field is not provided or invalid, try to auto-detect it
        try:
            polygon_fields_info = [f for f in arcpy.ListFields(polygons_fc) if f.type not in ("Geometry",)]
            polygon_field_names = [f.name for f in polygon_fields_info]
        except Exception:
            polygon_fields_info = []
            polygon_field_names = []

        if not name_field or name_field not in polygon_field_names:
            arcpy.AddMessage("Auto-detecting name field from polygons...")
            # Prefer string fields for matching
            string_fields = [f.name for f in polygon_fields_info if f.type == "String"]
            candidate_fields = string_fields or [
                f.name for f in polygon_fields_info if f.type not in ("OID", "GlobalID")
            ]

            match_count_by_field = {fname: 0 for fname in candidate_fields}
            if candidate_fields and name_value:
                try:
                    with arcpy.da.SearchCursor(polygons_fc, candidate_fields) as cursor:
                        name_value_cmp = name_value if case_sensitive else (name_value or "").lower()
                        for row in cursor:
                            for idx, fname in enumerate(candidate_fields):
                                val = row[idx]
                                if val is None:
                                    continue
                                if case_sensitive:
                                    if str(val) == name_value_cmp:
                                        match_count_by_field[fname] += 1
                                else:
                                    if str(val).lower() == name_value_cmp:
                                        match_count_by_field[fname] += 1
                except Exception:
                    pass

            # Pick the field with the highest match count (>0), else prefer common names, else first string field
            chosen_field = None
            if match_count_by_field:
                best_field = max(match_count_by_field, key=lambda k: match_count_by_field[k])
                if match_count_by_field[best_field] > 0:
                    chosen_field = best_field

            if not chosen_field and candidate_fields:
                common_names_ordered = [
                    "NAME", "Name", "name",
                    "DIST_NAME", "DISTRICT", "District", "district",
                    "ADM1_EN", "ADM2_EN", "STATE", "STATE_NAME",
                    "GN_NAME", "GEO_NAME", "LABEL", "LABEL_NAME",
                ]
                for candidate in common_names_ordered:
                    if candidate in candidate_fields:
                        chosen_field = candidate
                        break

            if not chosen_field and candidate_fields:
                chosen_field = candidate_fields[0]

            if chosen_field:
                name_field = chosen_field
                try:
                    parameters[2].value = chosen_field
                except Exception:
                    pass
                arcpy.AddMessage("Using field: {}".format(name_field))
            else:
                raise ValueError(
                    "Could not determine a valid name field from polygons. Please specify it explicitly."
                )

        arcpy.AddMessage("Selecting polygons by name...")
        delimited = arcpy.AddFieldDelimiters("polygons_lyr", name_field)
        where_clause = None

        if case_sensitive:
            where_clause = "{} = '{}'".format(delimited, name_value.replace("'", "''"))
        else:
            try:
                where_clause = "UPPER({}) = UPPER('{}')".format(delimited, name_value.replace("'", "''"))
                arcpy.management.SelectLayerByAttribute("polygons_lyr", "NEW_SELECTION", where_clause)
            except Exception:
                matches = set()
                with arcpy.da.SearchCursor(polygons_fc, [name_field]) as cursor:
                    name_value_lower = (name_value or "").lower()
                    for (val,) in cursor:
                        if val is not None and str(val).lower() == name_value_lower:
                            matches.add(str(val))
                if matches:
                    quoted = ", ".join(["'{}'".format(m.replace("'", "''")) for m in sorted(matches)])
                    where_clause = "{} IN ({})".format(delimited, quoted)
                else:
                    where_clause = "1 = 0"

        arcpy.management.SelectLayerByAttribute("polygons_lyr", "NEW_SELECTION", where_clause)
        poly_count = int(arcpy.management.GetCount("polygons_lyr")[0])
        if poly_count == 0:
            arcpy.AddWarning("No polygons matched the given name. Nothing to export.")
            return

        arcpy.AddMessage("Selected polygons: {}".format(poly_count))

        overlap_type = "WITHIN" if (predicate or "").upper() == "WITHIN" else "INTERSECT"
        arcpy.AddMessage("Selecting points by location: {} ...".format(overlap_type))
        arcpy.management.SelectLayerByLocation("points_lyr", overlap_type, "polygons_lyr", selection_type="NEW_SELECTION")

        pt_count = int(arcpy.management.GetCount("points_lyr")[0])
        if pt_count == 0:
            arcpy.AddWarning("No points satisfied the spatial selection. CSV will be empty.")

        fields_info = [f for f in arcpy.ListFields(points_fc) if f.type not in ("Geometry",)]
        oid_field = arcpy.Describe(points_fc).OIDFieldName
        field_names = [f.name for f in fields_info]
        field_aliases = [f.aliasName for f in fields_info]
        if oid_field in field_names:
            idx = field_names.index(oid_field)
            field_names.insert(0, field_names.pop(idx))
            field_aliases.insert(0, field_aliases.pop(idx))

        out_dir = arcpy.env.scratchFolder or arcpy.env.scratchGDB
        if not out_dir:
            out_dir = os.getcwd()
        out_csv_path = os.path.join(out_dir, "Output_data.csv")
        arcpy.AddMessage("Writing CSV (overwrite): {}".format(out_csv_path))

        with open(out_csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(field_aliases)
            with arcpy.da.SearchCursor("points_lyr", field_names) as cursor:
                for row in cursor:
                    writer.writerow(list(row))

        arcpy.SetParameterAsText(6, out_csv_path)

        arcpy.AddMessage("Done.")
        return

