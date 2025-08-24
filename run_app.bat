@echo off
echo ========================================
echo   GIS Point-in-Polygon Application
echo   Automated Setup and Run Script
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)
echo Python found: 
python --version

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo WARNING: Some packages may have failed to install
    echo Trying individual installation...
    pip install Flask>=2.3.0
    pip install geopandas>=0.14.0  
    pip install fiona>=1.9.0
    pip install pandas>=2.0.0
    pip install shapely>=2.0.0
    pip install pyproj>=3.5.0
)

echo.
echo [3/4] Testing installation...
python -c "import flask, geopandas, fiona; print('✅ All dependencies OK!')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Some dependencies are missing. Please check the output above.
    pause
    exit /b 1
)

echo.
echo [4/4] Starting the application...
echo.
echo ========================================
echo   🚀 GIS Application Starting...
echo ========================================
echo   📍 URL: http://127.0.0.1:5000
echo   🔧 Debug mode: ON
echo   ⏹️  Stop: Press Ctrl+C
echo ========================================
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5000

echo Starting Flask server...
python web_app.py