#!/usr/bin/env python
"""
Extract all point features that fall inside a polygon selected by name and export them to CSV.

Usage example (PowerShell on Windows):

  python extract_points_in_polygon.py \
    --points "C:\\data\\points.shp" \
    --polygons "C:\\data\\districts.shp" \
    --name-column "NAME" \
    --name-value "bankura" \
    --output "C:\\data\\bankura_points.csv"

Supported vector formats: any that GeoPandas/Fiona can read (e.g., Shapefile, GeoPackage, GeoJSON, etc.).
"""

import argparse
import sys
from typing import List

import geopandas as gpd
from shapely.geometry import base as shapely_base


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export points that fall inside a named polygon to CSV."
    )
    parser.add_argument(
        "--points",
        required=True,
        help="Path to the point layer (e.g., .shp, .gpkg, .geojson)",
    )
    parser.add_argument(
        "--points-layer",
        required=False,
        default=None,
        help="Optional: layer name inside a multi-layer file (e.g., GeoPackage) for points",
    )
    parser.add_argument(
        "--polygons",
        required=True,
        help="Path to the polygon layer (e.g., .shp, .gpkg, .geojson)",
    )
    parser.add_argument(
        "--polygons-layer",
        required=False,
        default=None,
        help="Optional: layer name inside a multi-layer file (e.g., GeoPackage) for polygons",
    )
    parser.add_argument(
        "--name-column",
        required=True,
        help="Attribute/field name in the polygon layer that contains the names (e.g., NAME)",
    )
    parser.add_argument(
        "--name-value",
        required=True,
        help="Name to match in the polygon layer (e.g., bankura)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the output CSV file",
    )
    parser.add_argument(
        "--predicate",
        choices=["within", "intersects"],
        default="within",
        help="Spatial predicate to use for selection (default: within)",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Make the name match case-sensitive (default: case-insensitive)",
    )
    return parser.parse_args(argv)


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
    # unary_union returns a single (possibly multi-) geometry
    return polygons.unary_union


def select_points(points: gpd.GeoDataFrame, geom: shapely_base.BaseGeometry, predicate: str) -> gpd.GeoDataFrame:
    if predicate == "within":
        mask = points.within(geom)
    elif predicate == "intersects":
        mask = points.intersects(geom)
    else:
        raise ValueError(f"Unsupported predicate: {predicate}")
    return points[mask]


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    print("Reading layers...")
    read_points_kwargs = {"layer": args.points_layer} if args.points_layer else {}
    read_polygons_kwargs = {"layer": args.polygons_layer} if args.polygons_layer else {}
    points = gpd.read_file(args.points, **read_points_kwargs)
    polygons = gpd.read_file(args.polygons, **read_polygons_kwargs)

    print("Checking and aligning CRS...")
    points = ensure_crs_compatible(points, polygons)

    print(f"Filtering polygons where {args.name_column} == '{args.name_value}' (case {'sensitive' if args.case_sensitive else 'insensitive'})...")
    matched_polygons = filter_polygons_by_name(
        polygons, args.name_column, args.name_value, args.case_sensitive
    )

    if matched_polygons.empty:
        print("No polygon matched the given name. Exiting.")
        return 2

    union_geom = build_union_geometry(matched_polygons)

    print(f"Selecting points that {args.predicate} the target polygon geometry...")
    selected_points = select_points(points, union_geom, args.predicate)

    # Prepare output DataFrame without geometry
    print(f"Writing {len(selected_points)} records to CSV: {args.output}")
    df_out = selected_points.drop(columns=["geometry"], errors="ignore")
    # Ensure index not written
    df_out.to_csv(args.output, index=False, encoding="utf-8")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

