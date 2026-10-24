
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import geometry_mask

PROJECT_DIR = Path(__file__).resolve().parents[1]

RASTER_PATH = (
    PROJECT_DIR / "data" / "processed"
    / "Three_Mandals_NDVI_Clipped_20261009.tif"
)

BOUNDARY_PATH = (
    PROJECT_DIR / "data" / "processed"
    / "Three_Mandals_Study_Area.geojson"
)

OUTPUT_DIR = PROJECT_DIR / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SUMMARY_PATH = OUTPUT_DIR / "ndvi_mandal_comparison.csv"
CLASSES_PATH = OUTPUT_DIR / "ndvi_class_distribution_by_mandal.csv"

classes = [
    ("Class 1", "Below 0.00", -np.inf, 0.00),
    ("Class 2", "0.00 to <0.15", 0.00, 0.15),
    ("Class 3", "0.15 to <0.30", 0.15, 0.30),
    ("Class 4", "0.30 to <0.45", 0.30, 0.45),
    ("Class 5", "0.45 and above", 0.45, np.inf),
]

print("Loading mandal boundaries and NDVI raster...")

boundaries = gpd.read_file(BOUNDARY_PATH)

summary_rows = []
class_rows = []

with rasterio.open(RASTER_PATH) as src:
    ndvi = src.read(1, masked=True)
    values = np.ma.getdata(ndvi)
    raster_valid = (
        ~np.ma.getmaskarray(ndvi)
        & np.isfinite(values)
    )

    pixel_area_m2 = abs(
        src.transform.a * src.transform.e
        - src.transform.b * src.transform.d
    )

    pixel_area_km2 = pixel_area_m2 / 1_000_000

    boundaries = boundaries.to_crs(src.crs)

    for _, feature in boundaries.iterrows():
        mandal = feature["mandal_name"]
        geometry = feature.geometry

        inside = geometry_mask(
            [geometry],
            out_shape=(src.height, src.width),
            transform=src.transform,
            invert=True,
            all_touched=False,
        )

        total_pixels = int(inside.sum())
        valid_mask = inside & raster_valid
        valid_values = values[valid_mask]
        valid_pixels = len(valid_values)

        if total_pixels == 0 or valid_pixels == 0:
            print(f"WARNING: No valid pixels for {mandal}")
            continue

        valid_area_km2 = valid_pixels * pixel_area_km2
        valid_coverage = valid_pixels / total_pixels * 100

        summary_rows.append({
            "Mandal": mandal,
            "Boundary_Pixels": total_pixels,
            "Valid_Pixels": valid_pixels,
            "Valid_Coverage_Percent": round(valid_coverage, 2),
            "Valid_Area_km2": round(valid_area_km2, 3),
            "Mean_NDVI": round(float(np.mean(valid_values)), 4),
            "Median_NDVI": round(float(np.median(valid_values)), 4),
            "Std_Dev_NDVI": round(float(np.std(valid_values)), 4),
            "Minimum_NDVI": round(float(np.min(valid_values)), 4),
            "Maximum_NDVI": round(float(np.max(valid_values)), 4),
        })

        for class_name, description, lower, upper in classes:
            class_mask = (
                valid_mask
                & (values >= lower)
                & (values < upper)
            )

            count = int(class_mask.sum())
            area_km2 = count * pixel_area_km2
            percentage = count / valid_pixels * 100

            class_rows.append({
                "Mandal": mandal,
                "NDVI_Class": class_name,
                "NDVI_Range": description,
                "Pixel_Count": count,
                "Area_km2": round(area_km2, 3),
                "Percentage_of_Mandal_Valid_Area": round(
                    percentage, 2
                ),
            })

summary = pd.DataFrame(summary_rows)
class_distribution = pd.DataFrame(class_rows)

summary.to_csv(SUMMARY_PATH, index=False)
class_distribution.to_csv(CLASSES_PATH, index=False)

print("\n" + "=" * 72)
print("NDVI COMPARISON BY MANDAL")
print("=" * 72)

if not summary.empty:
    print(
        summary[
            [
                "Mandal",
                "Valid_Coverage_Percent",
                "Valid_Area_km2",
                "Mean_NDVI",
                "Median_NDVI",
            ]
        ].to_string(index=False)
    )

print("\n" + "=" * 72)
print("NDVI CLASS DISTRIBUTION BY MANDAL")
print("=" * 72)

if not class_distribution.empty:
    print(
        class_distribution[
            [
                "Mandal",
                "NDVI_Class",
                "Area_km2",
                "Percentage_of_Mandal_Valid_Area",
            ]
        ].to_string(index=False)
    )

print("\nSaved files:")
print(SUMMARY_PATH)
print(CLASSES_PATH)
print("\nMandal comparison complete.")
