#!/usr/bin/env python3
"""
Diagnostic tool to inspect ZIP file contents and determine if they contain valid Shapefiles
"""

import zipfile
import os
import sys
from pathlib import Path

def diagnose_zip_file(zip_path):
    """Diagnose what's inside a ZIP file"""
    print(f"Analyzing ZIP file: {zip_path}")
    print("=" * 60)
    
    if not os.path.exists(zip_path):
        print(f"❌ ERROR: File not found: {zip_path}")
        return False
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            print(f"📂 Total files in ZIP: {len(file_list)}")
            print("\n📋 File listing:")
            
            shp_files = []
            shx_files = []
            dbf_files = []
            prj_files = []
            other_files = []
            
            for file_name in file_list:
                print(f"   • {file_name}")
                
                if file_name.lower().endswith('.shp'):
                    shp_files.append(file_name)
                elif file_name.lower().endswith('.shx'):
                    shx_files.append(file_name)
                elif file_name.lower().endswith('.dbf'):
                    dbf_files.append(file_name)
                elif file_name.lower().endswith('.prj'):
                    prj_files.append(file_name)
                else:
                    other_files.append(file_name)
            
            print("\n🔍 Shapefile Component Analysis:")
            print(f"   🗺️  .shp files (geometry): {len(shp_files)}")
            print(f"   📊 .shx files (index): {len(shx_files)}")
            print(f"   📋 .dbf files (attributes): {len(dbf_files)}")
            print(f"   🌐 .prj files (projection): {len(prj_files)}")
            print(f"   📄 Other files: {len(other_files)}")
            
            # Check for valid Shapefile structure
            is_valid_shapefile = False
            if len(shp_files) >= 1 and len(shx_files) >= 1 and len(dbf_files) >= 1:
                print("\n✅ GOOD NEWS: This ZIP contains the required Shapefile components!")
                is_valid_shapefile = True
            else:
                print("\n❌ PROBLEM: This ZIP is missing required Shapefile components!")
                print("   Required files for a valid Shapefile:")
                print("   • .shp file (geometry) - REQUIRED")
                print("   • .shx file (index) - REQUIRED") 
                print("   • .dbf file (attributes) - REQUIRED")
                print("   • .prj file (projection) - RECOMMENDED")
            
            # Check for folder structure issues
            folders_in_zip = [f for f in file_list if f.endswith('/') or '/' in f]
            if folders_in_zip:
                print(f"\n⚠️  WARNING: ZIP contains folder structure:")
                for folder in folders_in_zip[:5]:  # Show first 5
                    print(f"   📁 {folder}")
                if len(folders_in_zip) > 5:
                    print(f"   ... and {len(folders_in_zip) - 5} more")
                print("   💡 TIP: Shapefile components should be at the root level of the ZIP")
            
            return is_valid_shapefile
            
    except zipfile.BadZipFile:
        print("❌ ERROR: This is not a valid ZIP file or it's corrupted")
        return False
    except Exception as e:
        print(f"❌ ERROR: Unable to read ZIP file: {e}")
        return False

def main():
    # Check uploads directory for ZIP files
    uploads_dir = Path("uploads")
    if uploads_dir.exists():
        zip_files = list(uploads_dir.glob("*.zip"))
        if zip_files:
            print("🔍 Found ZIP files in uploads directory:")
            for i, zip_file in enumerate(zip_files, 1):
                print(f"\n{i}. {zip_file.name}")
                diagnose_zip_file(str(zip_file))
                print("\n" + "="*60)
        else:
            print("❌ No ZIP files found in uploads directory")
    else:
        print("❌ Uploads directory not found")
    
    # Also check if user provided a specific file
    if len(sys.argv) > 1:
        zip_path = sys.argv[1]
        diagnose_zip_file(zip_path)

if __name__ == "__main__":
    main()