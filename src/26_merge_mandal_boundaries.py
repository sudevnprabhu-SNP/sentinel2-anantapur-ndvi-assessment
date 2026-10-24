
from pathlib import Path

import geopandas as gpd
import rasterio


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_Masked_20261009.tif"
)

BOUNDARY_FILES = [
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_Urban_Rural_Bukkarayasamudram.geojson",

    PROJECT_DIR
    / "data"
    / "processed"
    / "Bukkaraya_Samudram.geojson",
]

OUTPUT_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Three_Mandals_Study_Area.geojson"
)


# ============================================================
# 2. CHECK INPUTS
# ============================================================

if not RASTER_PATH.exists():
    raise FileNotFoundError(f"Raster not found:\n{RASTER_PATH}")

for file_path in BOUNDARY_FILES:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Boundary file not found:\n{file_path}"
        )


# ============================================================
# 3. GET RASTER CRS
# ============================================================

with rasterio.open(RASTER_PATH) as raster:
    raster_crs = raster.crs

print("\nSentinel-2 raster CRS:", raster_crs)


# ============================================================
# 4. LOAD AND COMBINE BOUNDARIES
# ============================================================

boundary_layers = []

for file_path in BOUNDARY_FILES:
    print(f"\nReading: {file_path.name}")

    layer = gpd.read_file(file_path)

    if layer.empty:
        raise ValueError(
            f"No boundary features found in {file_path.name}"
        )

    if "mandal_name" not in layer.columns:
        raise ValueError(
            f"'mandal_name' field missing in {file_path.name}"
        )

    layer = layer.to_crs(raster_crs)
    boundary_layers.append(layer)

combined = gpd.GeoDataFrame(
    gpd.pd.concat(boundary_layers, ignore_index=True),
    geometry="geometry",
    crs=raster_crs,
)

# Keep one feature per mandal.
combined = combined.drop_duplicates(
    subset=["mandal_name"]
).reset_index(drop=True)

expected_mandals = {
    "Anantapur Urban",
    "Anantapur Rural",
    "Bukkaraya Samudram",
}

found_mandals = set(combined["mandal_name"].tolist())

missing_mandals = expected_mandals - found_mandals

if missing_mandals:
    raise ValueError(
        f"Missing expected mandals: {sorted(missing_mandals)}"
    )


# ============================================================
# 5. SAVE COMBINED BOUNDARIES
# ============================================================

combined.to_file(OUTPUT_PATH, driver="GeoJSON")

print("\n" + "=" * 55)
print("BOUNDARY MERGE COMPLETE")
print("=" * 55)

print("Mandals included:")

for name in combined["mandal_name"]:
    print(" -", name)

print(f"\nNumber of boundary features: {len(combined)}")
print(f"Output CRS: {combined.crs}")
print(f"Output file:\n{OUTPUT_PATH}")


# ============================================================
# 6. VERIFY SAVED FILE
# ============================================================

verified = gpd.read_file(OUTPUT_PATH)

print("\nVerification:")
print("Saved features:", len(verified))
print("Saved mandals:", verified["mandal_name"].tolist())
print("File exists:", OUTPUT_PATH.exists())

print("\nNext output:")
print("Three_Mandals_Study_Area.geojson")
