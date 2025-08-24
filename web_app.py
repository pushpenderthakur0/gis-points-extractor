import io
import os
import uuid
import zipfile
import tempfile
from typing import Optional

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import geopandas as gpd
from shapely.geometry import base as shapely_base
try:
    import fiona
except ImportError:
    fiona = None


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-in-production")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Max upload size: 200 MB
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024


def _allowed_extension(filename: str) -> bool:
    filename_lower = filename.lower()
    return filename_lower.endswith((".gpkg", ".geojson", ".json", ".zip", ".shp"))


def read_vector_layer(path: str, layer_name: Optional[str] = None) -> gpd.GeoDataFrame:
    lower = path.lower()
    if lower.endswith(".zip"):
        # Zipped shapefile - try different approaches
        try:
            # Method 1: Direct zip reading
            return gpd.read_file(f"zip://{path}")
        except Exception as e1:
            try:
                # Method 2: Try without zip prefix
                return gpd.read_file(path)
            except Exception as e2:
                try:
                    # Method 3: Try with fiona listing layers first (if available)
                    if fiona:
                        layers = fiona.listlayers(path)
                        if layers:
                            # Try each layer found
                            for layer in layers:
                                try:
                                    return gpd.read_file(path, layer=layer)
                                except:
                                    continue
                        else:
                            raise ValueError(f"No valid layers found in ZIP file.")
                    else:
                        raise ValueError(f"Could not read ZIP file. Make sure it contains a valid Shapefile (.shp, .shx, .dbf files).")
                except Exception as e3:
                    # Method 4: Try to extract and find .shp files manually
                    try:
                        with tempfile.TemporaryDirectory() as temp_dir:
                            # Extract the ZIP file
                            with zipfile.ZipFile(path, 'r') as zip_ref:
                                zip_ref.extractall(temp_dir)
                            
                            # Find .shp files recursively
                            shp_files = []
                            for root, dirs, files in os.walk(temp_dir):
                                for file in files:
                                    if file.lower().endswith('.shp'):
                                        shp_files.append(os.path.join(root, file))
                            
                            if shp_files:
                                # Try to read the first .shp file found
                                return gpd.read_file(shp_files[0])
                            else:
                                raise ValueError("No .shp files found in the ZIP archive")
                    except Exception as e4:
                        raise ValueError(f"Could not read ZIP file. Make sure it contains a valid Shapefile (.shp, .shx, .dbf files). Errors: {str(e1)}, {str(e2)}, {str(e3)}, {str(e4)}")
    
    if layer_name:
        return gpd.read_file(path, layer=layer_name)
    return gpd.read_file(path)


def ensure_crs_compatible(points: gpd.GeoDataFrame, polygons: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if polygons.crs is None and points.crs is None:
        raise ValueError("Both layers are missing CRS. Please define CRS for your data.")
    if polygons.crs is None:
        raise ValueError("Polygon layer CRS is missing. Please define it before running.")
    if points.crs is None:
        raise ValueError("Point layer CRS is missing. Please define it before running.")
    if points.crs != polygons.crs:
        points = points.to_crs(polygons.crs)
    return points


def filter_polygons_by_name(polygons: gpd.GeoDataFrame, name_column: str, name_value: str, case_sensitive: bool) -> gpd.GeoDataFrame:
    if name_column not in polygons.columns:
        raise KeyError(
            f"Column '{name_column}' not found in polygons. Available columns: {list(polygons.columns)}"
        )
    if case_sensitive:
        mask = polygons[name_column] == name_value
    else:
        mask = polygons[name_column].astype(str).str.lower() == str(name_value).lower()
    return polygons[mask]


def build_union_geometry(polygons: gpd.GeoDataFrame) -> shapely_base.BaseGeometry:
    if polygons.empty:
        raise ValueError("No polygons matched the given name.")
    # Use union_all() method instead of deprecated unary_union
    try:
        return polygons.union_all()
    except AttributeError:
        # Fallback for older versions of geopandas
        return polygons.unary_union


def select_points(points: gpd.GeoDataFrame, geom: shapely_base.BaseGeometry, predicate: str) -> gpd.GeoDataFrame:
    if predicate == "within":
        mask = points.within(geom)
    elif predicate == "intersects":
        mask = points.intersects(geom)
    else:
        raise ValueError(f"Unsupported predicate: {predicate}")
    return points[mask]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/run", methods=["POST"])
def run_tool():
    try:
        points_file = request.files.get("points_file")
        polygons_file = request.files.get("polygons_file")
        if not points_file or not polygons_file:
            flash("Please upload both points and polygons files.")
            return redirect(url_for("index"))

        if not (_allowed_extension(points_file.filename) and _allowed_extension(polygons_file.filename)):
            flash("Unsupported file type. Use GeoPackage (.gpkg), GeoJSON (.geojson/.json), or zipped Shapefile (.zip).")
            return redirect(url_for("index"))

        unique_prefix = uuid.uuid4().hex
        points_path = os.path.join(UPLOAD_DIR, f"{unique_prefix}_" + secure_filename(points_file.filename))
        polygons_path = os.path.join(UPLOAD_DIR, f"{unique_prefix}_" + secure_filename(polygons_file.filename))
        points_file.save(points_path)
        polygons_file.save(polygons_path)

        points_layer = request.form.get("points_layer") or None
        polygons_layer = request.form.get("polygons_layer") or None
        name_column = request.form.get("name_column", "").strip()
        name_value = request.form.get("name_value", "").strip()
        predicate = request.form.get("predicate", "within")
        case_sensitive = request.form.get("case_sensitive") == "on"

        if not name_column or not name_value:
            flash("Both 'Name column' and 'Name value' are required.")
            return redirect(url_for("index"))

        # Read and process data
        print(f"Reading points from: {points_path}")
        points = read_vector_layer(points_path, points_layer)
        print(f"Successfully read {len(points)} points")
        
        print(f"Reading polygons from: {polygons_path}")
        polygons = read_vector_layer(polygons_path, polygons_layer)
        print(f"Successfully read {len(polygons)} polygons")

        points = ensure_crs_compatible(points, polygons)
        matched_polygons = filter_polygons_by_name(polygons, name_column, name_value, case_sensitive)

        if matched_polygons.empty:
            flash(f"No polygon matched the name '{name_value}' in column '{name_column}'. Try a different value or check spelling.")
            return redirect(url_for("index"))

        print(f"Found {len(matched_polygons)} matching polygons")
        union_geom = build_union_geometry(matched_polygons)
        selected_points = select_points(points, union_geom, predicate)
        print(f"Selected {len(selected_points)} points using {predicate} predicate")

        # Prepare CSV output
        df_out = selected_points.drop(columns=["geometry"], errors="ignore")
        csv_stream = io.StringIO()
        df_out.to_csv(csv_stream, index=False, encoding="utf-8")
        csv_bytes = io.BytesIO(csv_stream.getvalue().encode("utf-8"))
        
        # Clean filename for download
        safe_name_value = "".join(c for c in name_value if c.isalnum() or c in (' ', '-', '_')).rstrip()
        download_name = f"{safe_name_value}_points.csv" if safe_name_value else "selected_points.csv"

        # Clean up uploaded files
        try:
            os.remove(points_path)
            os.remove(polygons_path)
        except:
            pass  # Ignore cleanup errors

        print(f"Sending CSV download: {download_name} with {len(df_out)} records")
        return send_file(
            csv_bytes,
            mimetype="text/csv",
            as_attachment=True,
            download_name=download_name,
        )
        
    except Exception as exc:
        print(f"Error in run_tool: {str(exc)}")
        import traceback
        traceback.print_exc()
        
        # Clean up files on error
        try:
            if 'points_path' in locals():
                os.remove(points_path)
            if 'polygons_path' in locals():
                os.remove(polygons_path)
        except:
            pass
            
        flash(f"Error processing your request: {str(exc)}")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

