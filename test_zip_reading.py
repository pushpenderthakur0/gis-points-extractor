#!/usr/bin/env python3
"""
Test the updated ZIP file reading functionality
"""

import sys
import os
sys.path.append('.')

from web_app import read_vector_layer

def test_zip_reading():
    # Test with the problematic ZIP files
    uploads_dir = "uploads"
    
    test_files = [
        "154da9d2c2314366a44b5a34811d440c_CWUA_Polygon.zip",
        "154da9d2c2314366a44b5a34811d440c_New_folder.zip"
    ]
    
    for test_file in test_files:
        file_path = os.path.join(uploads_dir, test_file)
        if os.path.exists(file_path):
            print(f"\\n🧪 Testing: {test_file}")
            print("-" * 50)
            try:
                gdf = read_vector_layer(file_path)
                print(f"✅ SUCCESS! Read {len(gdf)} features")
                print(f"   Columns: {list(gdf.columns)}")
                print(f"   Geometry type: {gdf.geometry.geom_type.iloc[0] if len(gdf) > 0 else 'N/A'}")
                print(f"   CRS: {gdf.crs}")
            except Exception as e:
                print(f"❌ FAILED: {e}")
        else:
            print(f"⚠️  File not found: {file_path}")

if __name__ == "__main__":
    test_zip_reading()