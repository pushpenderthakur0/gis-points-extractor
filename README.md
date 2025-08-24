# 🗺️ GIS Points Extractor

A modern web application for advanced geospatial analysis that extracts points within polygon boundaries and exports results to CSV format.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Flask](https://img.shields.io/badge/flask-2.3+-red.svg)
![GeoPandas](https://img.shields.io/badge/geopandas-0.14+-orange.svg)

## 🌟 Features

- **🎯 Point-in-Polygon Analysis**: Extract points that fall within specific polygonal areas
- **📊 Multiple File Format Support**: GeoPackage (.gpkg), GeoJSON (.geojson/.json), Shapefiles (.zip)
- **⚡ Fast Processing**: Optimized spatial analysis using GeoPandas and Shapely
- **📥 CSV Export**: Results ready for Excel, R, Python analysis
- **🌐 Modern Web Interface**: Responsive design with professional UI
- **🔒 Secure Processing**: Local data processing, no external servers
- **📱 Mobile Friendly**: Works on desktop, tablet, and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/gis-points-extractor.git
   cd gis-points-extractor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python web_app.py
   ```

4. **Open your browser**
   ```
   http://127.0.0.1:5000
   ```

## 📖 Usage

### Step 1: Upload Files
- **Points Layer**: Upload your point data (facilities, locations, etc.)
- **Polygon Layer**: Upload boundary data (districts, administrative areas, etc.)

### Step 2: Configure Selection
- **Name Column**: Field name in polygon layer (e.g., "district", "NAME")
- **Name Value**: Specific area name to analyze (e.g., "bankura", "kolkata")
- **Spatial Relationship**: Choose "within" or "intersects"

### Step 3: Process & Download
- Click "Process Data & Download CSV"
- Wait for processing to complete
- CSV file downloads automatically

## 🗂️ Supported File Formats

| Format | Extension | Recommendation |
|--------|-----------|----------------|
| GeoPackage | `.gpkg` | ⭐ **Recommended** - Single file, best performance |
| GeoJSON | `.geojson`, `.json` | ✅ Good - Web standard format |
| Shapefile | `.zip` | ⚠️ Requires .shp, .shx, .dbf files in ZIP |

## 🏗️ Project Structure

```
gis-points-extractor/
├── web_app.py                 # Main Flask application
├── extract_points_in_polygon.py  # Standalone script version
├── Point to CSV.pyt           # ArcGIS Python toolbox
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html            # Web interface template
├── uploads/                  # Temporary file storage
├── docs/                     # Documentation
│   ├── HOW_TO_RUN.md        # Detailed setup guide
│   ├── TROUBLESHOOTING.md   # Common issues & solutions
│   └── FEATURE_GUIDE.md     # Feature documentation
└── README.md                # This file
```

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Geospatial**: GeoPandas, Shapely, Fiona, PyProj
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Icons**: Font Awesome
- **Fonts**: Inter (Google Fonts)

## 📋 Requirements

### Python Dependencies
```
Flask>=2.3.0
geopandas>=0.14.0
fiona>=1.9.0
pandas>=2.0.0
shapely>=2.0.0
pyproj>=3.5.0
```

### System Requirements
- **OS**: Windows, macOS, Linux
- **Python**: 3.8+
- **Memory**: 4GB RAM minimum (8GB recommended for large datasets)
- **Disk Space**: 1GB free space

## 🔧 Configuration

### Environment Variables (Optional)
```bash
export FLASK_SECRET_KEY="your-secret-key-here"
export FLASK_ENV=development  # or production
```

### File Upload Limits
- Maximum file size: 200MB
- Supported projections: Any EPSG code
- Coordinate systems: Automatic alignment

## 📊 Examples

### Command Line Usage
```bash
python extract_points_in_polygon.py \
  --points "data/schools.gpkg" \
  --polygons "data/districts.gpkg" \
  --name-column "DISTRICT_NAME" \
  --name-value "Mumbai" \
  --output "mumbai_schools.csv"
```

### API Usage (Programmatic)
```python
from web_app import read_vector_layer, filter_polygons_by_name

# Load data
points = read_vector_layer("schools.gpkg")
polygons = read_vector_layer("districts.gpkg")

# Filter and analyze
selected_polygons = filter_polygons_by_name(polygons, "NAME", "Mumbai", False)
# ... continue processing
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
git clone https://github.com/yourusername/gis-points-extractor.git
cd gis-points-extractor
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

## 🐛 Troubleshooting

### Common Issues

**File Format Errors**
- Ensure ZIP files contain .shp, .shx, .dbf files
- Use GeoPackage (.gpkg) format for best compatibility

**Processing Errors**
- Check that name column exists in polygon data
- Verify coordinate systems are valid
- Try smaller datasets first

**Performance Issues**
- Use simplified geometries for large datasets
- Consider GeoPackage format for better performance

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for detailed solutions.

## 📚 Documentation

- [📖 Setup Guide](docs/HOW_TO_RUN.md) - Detailed installation and setup
- [🔧 Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [✨ Features](docs/FEATURE_GUIDE.md) - Detailed feature documentation
- [🔄 Fixes Applied](docs/FIXES_APPLIED.md) - Recent improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GeoPandas** - For excellent geospatial data handling
- **Shapely** - For geometric operations
- **Flask** - For the web framework
- **Bootstrap** - For responsive UI components
- **Font Awesome** - For beautiful icons

## 📧 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/gis-points-extractor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/gis-points-extractor/discussions)

---

⭐ **Star this repository if you find it useful!**

## 🔗 Links

- [Live Demo](https://your-demo-site.com) (if available)
- [Documentation](https://your-docs-site.com) (if available)
- [PyPI Package](https://pypi.org/project/gis-points-extractor/) (if published)

---

**Made with ❤️ for the GIS community**