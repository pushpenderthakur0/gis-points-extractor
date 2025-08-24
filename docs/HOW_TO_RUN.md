# 🚀 How to Run the GIS Point-in-Polygon Application

## 📋 Prerequisites

### 1. Python Installation
- **Python 3.8 or higher** must be installed
- Check your Python version:
  ```cmd
  python --version
  ```

### 2. Command Line Access
- **Windows**: Use Command Prompt, PowerShell, or Terminal
- **Tip**: Press `Win + R`, type `cmd`, press Enter

## 🛠️ Step-by-Step Setup

### Step 1: Navigate to Project Directory
```cmd
cd "C:\Users\DELL\OneDrive - Sintu\Desktop\New folder (3)\New folder (3)"
```

### Step 2: Install Required Dependencies
```cmd
pip install -r requirements.txt
```

**Or install individually:**
```cmd
pip install Flask>=2.3.0
pip install geopandas>=0.14.0
pip install fiona>=1.9.0
pip install pandas>=2.0.0
pip install shapely>=2.0.0
pip install pyproj>=3.5.0
```

### Step 3: Run the Application
```cmd
python web_app.py
```

## 🌐 Accessing the Application

After running the command, you'll see output like:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

**Open your web browser** and go to: `http://127.0.0.1:5000`

## 🗂️ Alternative Running Methods

### Method 1: Direct Python Execution
```cmd
python web_app.py
```

### Method 2: Using Python Module
```cmd
python -m flask --app web_app run
```

### Method 3: With Custom Host/Port
```cmd
python -c "from web_app import app; app.run(host='0.0.0.0', port=5000, debug=True)"
```

## 🎯 Using the Application

### 1. **Upload Files**
- **Points file**: Your point data (schools, hospitals, etc.)
- **Polygons file**: Administrative boundaries (districts, blocks)
- **Supported formats**: `.gpkg`, `.geojson`, `.zip` (for Shapefiles)

### 2. **Configure Parameters**
- **Name column**: Field in polygon layer (e.g., "district", "NAME")
- **Name value**: Specific area name (e.g., "bankura", "kolkata")
- **Spatial predicate**: 
  - `within` - Points completely inside
  - `intersects` - Points touching or overlapping

### 3. **Download Results**
- Click "Run and download CSV"
- Get CSV file with selected points

## 🔧 Troubleshooting

### Problem: "pip not found"
**Solution**: 
```cmd
python -m pip install -r requirements.txt
```

### Problem: "Module not found" errors
**Solution**: Install missing packages individually:
```cmd
pip install package_name
```

### Problem: Permission errors
**Solution**: Run as administrator or use:
```cmd
pip install --user package_name
```

### Problem: Port already in use
**Solution**: Use different port:
```cmd
python -c "from web_app import app; app.run(port=5001)"
```

### Problem: ZIP file not reading
**Solution**: 
- Ensure ZIP contains `.shp`, `.shx`, `.dbf` files
- Or use `.gpkg` format (recommended)

## 📁 Project File Structure
```
New folder (3)/
├── web_app.py              # Main Flask application
├── extract_points_in_polygon.py  # Standalone script
├── requirements.txt        # Dependencies list
├── templates/
│   └── index.html         # Web interface
├── uploads/               # Uploaded files storage
├── TROUBLESHOOTING.md     # Detailed troubleshooting
└── HOW_TO_RUN.md         # This guide
```

## 🎉 Quick Start Commands

**One-liner setup and run:**
```cmd
cd "C:\Users\DELL\OneDrive - Sintu\Desktop\New folder (3)\New folder (3)" && pip install -r requirements.txt && python web_app.py
```

## 🔄 Stopping the Application

To stop the server:
- Press `Ctrl + C` in the terminal
- Or close the command prompt window

## 🧪 Testing Your Setup

Test if everything works:
```cmd
python -c "import geopandas, flask; print('All dependencies OK!')"
```

## 💡 Pro Tips

1. **Keep terminal open** while using the web application
2. **Use `.gpkg` files** instead of ZIP for better compatibility  
3. **Check the terminal** for error messages if something goes wrong
4. **Debug mode** auto-reloads when you change code
5. **Access from other devices** using your IP address (e.g., `http://192.168.1.100:5000`)

## 🆘 Need Help?

1. Check `TROUBLESHOOTING.md` for common issues
2. Verify all dependencies are installed
3. Ensure Python version is 3.8+
4. Check file formats are supported
5. Look at terminal output for error messages

---

**That's it! Your GIS application should now be running! 🚀**