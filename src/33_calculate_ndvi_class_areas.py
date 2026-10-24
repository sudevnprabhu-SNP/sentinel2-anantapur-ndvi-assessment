
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]

RASTER_PATH = (
    PROJECT_DIR / "data" / "processed"
    / "Three_Mandals_NDVI_Classes_20261009.tif"
)

OUTPUT_CSV = (
    PROJECT_DIR / "reports"
    / "ndvi_class_area_statistics.csv"
)

OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Define class labels
# --------------------------------------------------

CLASS_NAMES = {
    1: "Below 0.00",
    2: "0.00 to < 0.15",
    3: "0.15 to < 0.30",
    4: "0.30 to < 0.45",
    5: "0.45 and above",
}

# --------------------------------------------------
# 3. Read raster and calculate pixel areas
# --------------------------------------------------

print("Reading classified NDVI raster...")

with rasterio.open(RASTER_PATH) as src:
    classes = src.read(1)
    pixel_width = abs(src.transform.a)
    pixel_height = abs(src.transform.e)
    crs = src.crs
    nodata = src.nodata

if crs is None or not crs.is_projected:
    raise ValueError(
        "The raster must use a projected CRS "
        "to calculate area in square metres."
    )

pixel_area_m2 = pixel_width * pixel_height
pixel_area_km2 = pixel_area_m2 / 1_000_000

valid_mask = classes > 0
total_valid_pixels = int(valid_mask.sum())
total_valid_area_km2 = total_valid_pixels * pixel_area_km2

print(f"CRS: {crs}")
print(f"Pixel size: {pixel_width:g} m x {pixel_height:g} m")
print(f"Area per pixel: {pixel_area_m2:g} m²")
print(f"Valid pixels: {total_valid_pixels:,}")
print(f"Total valid area: {total_valid_area_km2:.4f} km²")

# --------------------------------------------------
# 4. Calculate area for each class
# --------------------------------------------------

rows = []

for code, name in CLASS_NAMES.items():
    pixel_count = int((classes == code).sum())
    area_km2 = pixel_count * pixel_area_km2
    area_hectares = area_km2 * 100

    percentage = (
        pixel_count / total_valid_pixels * 100
        if total_valid_pixels else 0
    )

    rows.append({
        "Class_Code": code,
        "NDVI_Class": name,
        "Pixel_Count": pixel_count,
        "Area_Hectares": area_hectares,
        "Area_Square_Kilometres": area_km2,
        "Percentage_of_Valid_Area": percentage,
    })

df = pd.DataFrame(rows)

df.to_csv(OUTPUT_CSV, index=False, float_format="%.4f")

# --------------------------------------------------
# 5. Display and verify results
# --------------------------------------------------

print("\n" + "=" * 78)
print("AREA DISTRIBUTION BY NDVI CLASS")
print("=" * 78)

print(
    df.to_string(
        index=False,
        formatters={
            "Area_Hectares": "{:.2f}".format,
            "Area_Square_Kilometres": "{:.4f}".format,
            "Percentage_of_Valid_Area": "{:.2f}".format,
        },
    )
)

print("\nTotal class area: "
      f"{df['Area_Square_Kilometres'].sum():.4f} km²")

print(f"CSV saved to: {OUTPUT_CSV}")
print("\nNDVI class area calculation complete.")
