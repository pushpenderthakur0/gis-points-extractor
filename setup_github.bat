@echo off
echo ========================================
echo    GIS Points Extractor - GitHub Setup
echo ========================================
echo.

echo Step 1: Initializing Git repository...
git init
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo.
echo Step 2: Adding files to Git...
git add .
if %errorlevel% neq 0 (
    echo Error: Failed to add files to Git
    pause
    exit /b 1
)

echo.
echo Step 3: Making initial commit...
git commit -m "Initial commit: GIS Points Extractor web application"
if %errorlevel% neq 0 (
    echo Error: Failed to commit files
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Manual Steps Required
echo ========================================
echo.
echo 1. Go to https://github.com and create a new repository
echo    - Name: gis-points-extractor
echo    - Description: A modern web application for advanced geospatial analysis
echo    - Make it Public
echo    - DO NOT initialize with README (we already have one)
echo.
echo 2. After creating the repository, run these commands:
echo    git remote add origin https://github.com/YOUR_USERNAME/gis-points-extractor.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Replace YOUR_USERNAME with your actual GitHub username
echo.
echo 4. Update the following files with your information:
echo    - README.md (replace yourusername with your GitHub username)
echo    - setup.py (update author and email)
echo.
echo 5. Then run: git add . && git commit -m "Update repository info" && git push
echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo Your repository will be available at:
echo https://github.com/YOUR_USERNAME/gis-points-extractor
echo.
pause