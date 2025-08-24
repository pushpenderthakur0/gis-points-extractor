# 📁 Examples Directory

This directory contains example data files to help you test the GIS Points Extractor application.

## 🗂️ Example Files

### Sample Data Structure

```
examples/
├── points/
│   ├── schools_sample.gpkg      # Sample school locations
│   └── hospitals_sample.gpkg    # Sample hospital locations
├── polygons/
│   ├── districts_sample.gpkg    # Sample district boundaries
│   └── wards_sample.gpkg        # Sample ward boundaries
└── README.md                    # This file
```

## 🧪 Testing the Application

1. **Download sample data** from a reliable GIS data source
2. **Upload points file** (e.g., schools, hospitals, facilities)
3. **Upload polygons file** (e.g., districts, wards, administrative boundaries)
4. **Configure the analysis**:
   - Name Column: `NAME` or `DISTRICT_NAME`
   - Name Value: Enter a specific area name
5. **Process and download** the CSV results

## 📊 Sample Use Cases

### Education Analysis
- **Points**: School locations
- **Polygons**: District boundaries
- **Analysis**: Find all schools in a specific district

### Healthcare Planning
- **Points**: Hospital and clinic locations
- **Polygons**: Administrative wards
- **Analysis**: Healthcare facility distribution by ward

### Infrastructure Planning
- **Points**: Utility locations (water, electricity)
- **Polygons**: Municipal boundaries
- **Analysis**: Infrastructure coverage analysis

## 🔗 Data Sources

For sample data, you can use:
- [OpenStreetMap](https://www.openstreetmap.org/) - Free geographic data
- [Natural Earth](https://www.naturalearthdata.com/) - Public domain maps
- [GADM](https://gadm.org/) - Administrative boundaries
- [Government Open Data Portals](https://data.gov/) - Official datasets

## 📝 Data Format Requirements

- **GeoPackage (.gpkg)** - Recommended format
- **GeoJSON (.geojson/.json)** - Web standard
- **Shapefile (.zip)** - Traditional GIS format

Make sure your data includes:
- Valid geometries (points for points layer, polygons for polygon layer)
- Coordinate reference system (CRS) information
- Attribute fields for identification 