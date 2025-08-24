# Troubleshooting Guide

## File Format Error Solutions

### Error: "not recognized as being in a supported file format"

This error occurs when the uploaded file is not a valid geospatial format. Here are the solutions:

#### 1. For ZIP Files (Shapefiles)
**Problem**: ZIP file doesn't contain valid Shapefile components

**Solution**: Ensure your ZIP file contains ALL these files:
- `filename.shp` (geometry)
- `filename.shx` (index)
- `filename.dbf` (attributes)
- Optional: `filename.prj` (projection), `filename.cpg` (encoding)

#### 2. Recommended File Formats
Instead of ZIP files, use these more reliable formats:

**GeoPackage (.gpkg)** - RECOMMENDED
- Single file format
- Supports multiple layers
- Better performance
- Cross-platform compatibility

**GeoJSON (.geojson/.json)**
- Text-based format
- Web-friendly
- Good for smaller datasets

#### 3. Converting Your Data
If you have data in other formats, convert it first:

```python
# Convert Shapefile to GeoPackage
import geopandas as gpd
df = gpd.read_file("your_data.shp")
df.to_file("your_data.gpkg", driver="GPKG")
```

#### 4. Testing Your Files
Before uploading, test if your file is readable:

```python
import geopandas as gpd
try:
    df = gpd.read_file("your_file.gpkg")
    print(f"Success! Found {len(df)} features")
    print(f"Columns: {list(df.columns)}")
except Exception as e:
    print(f"Error: {e}")
```

#### 5. Common Issues and Fixes

**ZIP File Issues:**
- Make sure the ZIP contains actual Shapefile components, not folders
- Don't zip a folder containing the files - zip the files directly
- Use standard ZIP compression (not RAR, 7z, etc.)

**Encoding Issues:**
- Save your data with UTF-8 encoding
- Include a .cpg file specifying the encoding

**Coordinate System Issues:**
- Include a .prj file with projection information
- Or use formats like GeoPackage that store CRS information internally

## Need Help?
If you continue having issues:
1. Check your source data in QGIS or ArcGIS first
2. Try converting to GeoPackage format
3. Verify the file opens in other GIS software before uploading