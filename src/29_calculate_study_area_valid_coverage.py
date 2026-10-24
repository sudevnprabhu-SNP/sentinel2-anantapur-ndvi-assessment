
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import geometry_mask


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Three_Mandals_NDVI_Clipped_20261009.tif"
)

BOUNDARY_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Three_Mandals_Study_Area.geojson"
)


# ============================================================
# 2. CHECK INPUT FILES
# ============================================================

if not RASTER_PATH.exists():
    raise FileNotFoundError(f"NDVI raster not found:\n{RASTER_PATH}")

if not BOUNDARY_PATH.exists():
    raise FileNotFoundError(
        f"Study-area boundary not found:\n{BOUNDARY_PATH}"
    )


# ============================================================
# 3. READ BOUNDARIES AND RASTER
# ============================================================

print("\nReading study area and NDVI raster...")

boundaries = gpd.read_file(BOUNDARY_PATH)

if boundaries.empty:
    raise ValueError("The study-area boundary contains no features.")

with rasterio.open(RASTER_PATH) as src:
    raster = src.read(1, masked=True)
    transform = src.transform
    raster_crs = src.crs
    nodata = src.nodata

    # Convert boundaries into the raster's coordinate system.
    boundaries = boundaries.to_crs(raster_crs)

    # Combine all three mandals into one study-area geometry.
    study_area = boundaries.geometry.union_all()

    # True for pixels whose centres are inside the study area.
    inside_study_area = geometry_mask(
        [study_area],
        out_shape=(src.height, src.width),
        transform=transform,
        invert=True,
        all_touched=False,
    )

    # True for pixels that have valid, finite NDVI values.
    ndvi_values = np.ma.getdata(raster)
    raster_mask = np.ma.getmaskarray(raster)

    valid_ndvi = (
        ~raster_mask
        & np.isfinite(ndvi_values)
    )

    # Count only pixels inside the study area.
    study_area_pixels = inside_study_area.sum()

    valid_study_pixels = (
        inside_study_area & valid_ndvi
    ).sum()

    invalid_study_pixels = (
        inside_study_area & ~valid_ndvi
    ).sum()

    if study_area_pixels == 0:
        raise ValueError(
            "No raster pixels were found inside the study area."
        )

    valid_percentage = (
        valid_study_pixels / study_area_pixels
    ) * 100

    invalid_percentage = (
        invalid_study_pixels / study_area_pixels
    ) * 100

    valid_values = ndvi_values[
        inside_study_area & valid_ndvi
    ]


# ============================================================
# 4. PRINT COVERAGE RESULTS
# ============================================================

print("\n" + "=" * 60)
print("THREE-MANDAL VALID NDVI COVERAGE")
print("=" * 60)

print("Study area: Anantapur Urban, Anantapur Rural,")
print("            and Bukkaraya Samudram")

print(f"\nTotal pixels inside study area: {study_area_pixels:,}")
print(f"Valid NDVI pixels: {valid_study_pixels:,}")
print(f"Invalid / NoData pixels: {invalid_study_pixels:,}")

print(f"\nValid NDVI coverage: {valid_percentage:.2f}%")
print(f"Invalid / NoData percentage: {invalid_percentage:.2f}%")

if valid_values.size > 0:
    print("\n--- VALID NDVI STATISTICS ---")
    print(f"Minimum NDVI: {valid_values.min():.4f}")
    print(f"Maximum NDVI: {valid_values.max():.4f}")
    print(f"Mean NDVI: {valid_values.mean():.4f}")
    print(f"Median NDVI: {np.median(valid_values):.4f}")
    print(f"Standard deviation: {valid_values.std():.4f}")
else:
    print("\nWARNING: No valid NDVI pixels inside the study area.")

print("\nNote:")
print("- Pixels outside the three mandals are excluded.")
print("- NoData includes cloud-masked and other invalid pixels.")
print("- This is valid raster-data coverage, not a direct")
print("  measurement of cloud cover alone.")

print("\nCoverage calculation complete.")
