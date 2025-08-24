@echo off
echo ========================================
echo   GitHub Setup Script for GIS Project
echo ========================================
echo.

echo [Step 1] Checking if Git is installed...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed!
    echo.
    echo Please download and install Git from: https://git-scm.com/download/win
    echo After installation, run this script again.
    pause
    exit /b 1
) else (
    echo ✅ Git is installed
    git --version
)

echo.
echo [Step 2] Git Configuration
echo Please enter your details:
echo.

set /p USER_NAME="Enter your full name (e.g., John Doe): "
set /p USER_EMAIL="Enter your email (e.g., john@gmail.com): "

echo.
echo Configuring Git with your details...
git config --global user.name "%USER_NAME%"
git config --global user.email "%USER_EMAIL%"

echo ✅ Git configured successfully!
echo   Name: %USER_NAME%
echo   Email: %USER_EMAIL%

echo.
echo [Step 3] GitHub Repository Information
echo.
echo Before proceeding, please:
echo 1. Go to https://github.com
echo 2. Click "New repository" (green button)
echo 3. Repository name: gis-points-extractor (or your choice)
echo 4. Description: Modern web application for geospatial analysis
echo 5. Make it PUBLIC
echo 6. DON'T initialize with README, .gitignore, or license
echo 7. Click "Create repository"
echo.

set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter repository name (default: gis-points-extractor): "

if "%REPO_NAME%"=="" set REPO_NAME=gis-points-extractor

echo.
echo [Step 4] Initializing Git Repository...

rem Check if already a git repo
if exist ".git" (
    echo ⚠️ Git repository already exists. Skipping git init...
) else (
    git init
    echo ✅ Git repository initialized
)

echo.
echo [Step 5] Adding files to Git...
git add .
if %errorlevel% neq 0 (
    echo ❌ Error adding files to git
    pause
    exit /b 1
)
echo ✅ Files added to staging area

echo.
echo [Step 6] Creating initial commit...
git commit -m "Initial commit: GIS Points Extractor web application

- Modern Flask web interface for geospatial analysis
- Point-in-polygon extraction functionality  
- Multi-format support (GeoPackage, GeoJSON, Shapefile)
- Responsive design with Bootstrap 5
- ArcGIS Python toolbox included
- Comprehensive documentation"

if %errorlevel% neq 0 (
    echo ❌ Error creating commit
    pause
    exit /b 1
)
echo ✅ Initial commit created

echo.
echo [Step 7] Connecting to GitHub...
git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
if %errorlevel% neq 0 (
    echo ⚠️ Remote already exists or error occurred
    echo Removing existing remote and adding new one...
    git remote remove origin
    git remote add origin https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
)

echo ✅ Connected to GitHub repository
echo   Repository: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%

echo.
echo [Step 8] Setting main branch...
git branch -M main
echo ✅ Main branch set

echo.
echo [Step 9] Pushing to GitHub...
echo This will upload your code to GitHub...
echo.

git push -u origin main
if %errorlevel% neq 0 (
    echo.
    echo ❌ Error pushing to GitHub!
    echo.
    echo Possible reasons:
    echo 1. Repository doesn't exist on GitHub
    echo 2. Authentication required
    echo 3. Network connection issues
    echo.
    echo Solutions:
    echo 1. Make sure you created the repository on GitHub
    echo 2. You might need to authenticate with GitHub
    echo 3. Try running: git push -u origin main manually
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo           🎉 SUCCESS! 🎉
echo ========================================
echo.
echo ✅ Your GIS Points Extractor is now on GitHub!
echo.
echo 📍 Repository URL: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo.
echo Next steps:
echo 1. Visit your repository: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
echo 2. Add a description and topics (gis, geospatial, flask, python)
echo 3. Star your repository for visibility
echo 4. Share the link with others!
echo.
echo ========================================

pause