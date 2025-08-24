# -*- coding: utf-8 -*-
"""
ArcGIS Python Toolbox (.pyt) - Extract Points Inside Polygon to CSV

Add this toolbox in ArcGIS Pro (Catalog > Toolboxes > Add Toolbox...), then run the
tool: it filters polygons by a name field/value and exports all points that are
within/intersecting those polygons to a CSV file.
"""

import arcpy
import csv
import os


class Toolbox(object):
    def __init__(self):
        self.label = "Points-in-Polygon Export"
        self.alias = "points_in_polygon_export"
        self.tools = [ExtractPointsInPolygon]


class ExtractPointsInPolygon(object):
    def __init__(self):
        self.label = "Extract Points Inside Polygon to CSV"
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
        # Simple point default schema so GP services/WAB can draw inputs if needed
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
        # Simple polygon default schema so GP services/WAB can draw inputs if needed
        try:
            polygons_fc.schema = r"""
            {"geometryType": "esriGeometryPolygon", "fields": [{"name": "OBJECTID", "type": "esriFieldTypeOID"}]}
            """.strip()
        except Exception:
            pass

        name_field = arcpy.Parameter(
            displayName="Name field (in polygons)",
            name="name_field",
            datatype="Field",
            parameterType="Required",
            direction="Input",
        )
        name_field.parameterDependencies = ["polygons_fc"]

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
        # Output path will be created in the server scratch folder for GP services
        # and set as the derived output parameter

        arcpy.AddMessage("Making feature layers...")
        arcpy.management.MakeFeatureLayer(points_fc, "points_lyr")
        arcpy.management.MakeFeatureLayer(polygons_fc, "polygons_lyr")

        # Build attribute where clause for polygons
        arcpy.AddMessage("Selecting polygons by name...")
        delimited = arcpy.AddFieldDelimiters("polygons_lyr", name_field)
        where_clause = None

        if case_sensitive:
            # Direct equality
            where_clause = "{} = '{}'".format(delimited, name_value.replace("'", "''"))
        else:
            # Try case-insensitive via UPPER(); if it fails, fallback to IN (...) of exact matches
            try:
                where_clause = "UPPER({}) = UPPER('{}')".format(delimited, name_value.replace("'", "''"))
                arcpy.management.SelectLayerByAttribute("polygons_lyr", "NEW_SELECTION", where_clause)
                # If selection succeeded but count is zero, still acceptable; otherwise we proceed
            except Exception:
                # Fallback: build an IN (...) list of exact values matching case-insensitive
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
                    where_clause = "1 = 0"  # No match

        # Apply attribute selection
        arcpy.management.SelectLayerByAttribute("polygons_lyr", "NEW_SELECTION", where_clause)
        poly_count = int(arcpy.management.GetCount("polygons_lyr")[0])
        if poly_count == 0:
            arcpy.AddWarning("No polygons matched the given name. Nothing to export.")
            return

        arcpy.AddMessage("Selected polygons: {}".format(poly_count))

        # Spatial selection of points by location
        overlap_type = "WITHIN" if (predicate or "").upper() == "WITHIN" else "INTERSECT"
        arcpy.AddMessage("Selecting points by location: {} ...".format(overlap_type))
        arcpy.management.SelectLayerByLocation("points_lyr", overlap_type, "polygons_lyr", selection_type="NEW_SELECTION")

        pt_count = int(arcpy.management.GetCount("points_lyr")[0])
        if pt_count == 0:
            arcpy.AddWarning("No points satisfied the spatial selection. CSV will be empty.")

        # Prepare fields (exclude geometry and OID written twice)
        fields = [f.name for f in arcpy.ListFields(points_fc) if f.type not in ("Geometry",)]
        # Ensure a stable order: OID first if present
        oid_field = arcpy.Describe(points_fc).OIDFieldName
        if oid_field in fields:
            fields.remove(oid_field)
            fields.insert(0, oid_field)

        # Build output path in scratch folder; name based on value
        safe_name = (name_value or "selection").strip().replace(" ", "_")
        if not safe_name:
            safe_name = "selection"
        out_dir = arcpy.env.scratchFolder or arcpy.env.scratchGDB
        if not out_dir:
            out_dir = os.getcwd()
        out_csv_path = os.path.join(out_dir, "{}{}_points.csv".format("", safe_name))
        arcpy.AddMessage("Writing CSV: {}".format(out_csv_path))

        with open(out_csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            with arcpy.da.SearchCursor("points_lyr", fields) as cursor:
                for row in cursor:
                    writer.writerow(list(row))

        # Set derived output
        arcpy.SetParameterAsText(6, out_csv_path)

        arcpy.AddMessage("Done.")
        return

