
from pathlib import Path

import geopandas as gpd
import rasterio
from rasterio.mask import mask


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_RASTER = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_Masked_20261009.tif"
)

BOUNDARY_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Three_Mandals_Study_Area.geojson"
)

OUTPUT_RASTER = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Three_Mandals_NDVI_Clipped_20261009.tif"
)


# ============================================================
# 2. CHECK INPUT FILES
# ============================================================

if not INPUT_RASTER.exists():
    raise FileNotFoundError(
        f"Input NDVI raster not found:\n{INPUT_RASTER}"
    )

if not BOUNDARY_FILE.exists():
    raise FileNotFoundError(
        f"Study-area boundary not found:\n{BOUNDARY_FILE}"
    )


# ============================================================
# 3. READ AND PREPARE BOUNDARIES
# ============================================================

print("\nReading study-area boundaries...")

mandals = gpd.read_file(BOUNDARY_FILE)

if mandals.empty:
    raise ValueError("The boundary file contains no features.")

if mandals.crs is None:
    raise ValueError("The boundary file has no defined CRS.")

print("Mandals found:", mandals["mandal_name"].tolist())


# ============================================================
# 4. CLIP RASTER TO THE THREE MANDALS
# ============================================================

print("\nClipping NDVI raster...")

with rasterio.open(INPUT_RASTER) as src:

    print("Input raster CRS:", src.crs)
    print("Boundary CRS:", mandals.crs)

    # Reproject boundaries to match the raster.
    mandals = mandals.to_crs(src.crs)

    # Combine the three mandal geometries into one study area.
    study_area = mandals.geometry.union_all()

    # Keep the input raster's existing NoData value.
    nodata_value = (
        src.nodata if src.nodata is not None else -9999.0
    )

    # Clip the raster and fill pixels outside the study area.
    clipped_data, clipped_transform = mask(
        src,
        [study_area],
        crop=True,
        nodata=nodata_value,
        filled=True,
        all_touched=False,
    )

    # Prepare output metadata.
    output_meta = src.meta.copy()
    output_meta.update(
        {
            "driver": "GTiff",
            "height": clipped_data.shape[1],
            "width": clipped_data.shape[2],
            "transform": clipped_transform,
            "nodata": nodata_value,
            "compress": "deflate",
        }
    )

    # Save the clipped raster.
    with rasterio.open(OUTPUT_RASTER, "w", **output_meta) as dst:
        dst.write(clipped_data)


# ============================================================
# 5. REPORT RESULTS
# ============================================================

print("\n" + "=" * 55)
print("THREE-MANDAL NDVI CLIP COMPLETE")
print("=" * 55)

print("Output file:", OUTPUT_RASTER.name)
print("Saved location:", OUTPUT_RASTER)

with rasterio.open(OUTPUT_RASTER) as result:
    print("CRS:", result.crs)
    print("Dimensions:", result.width, "x", result.height)
    print("Pixel size:", result.res)
    print("NoData value:", result.nodata)
    print("Bounds:", result.bounds)

print("\nThe clipped NDVI raster is ready for verification.")
