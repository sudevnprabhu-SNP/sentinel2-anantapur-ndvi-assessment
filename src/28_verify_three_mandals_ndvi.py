
from pathlib import Path

import numpy as np
import rasterio


# ============================================================
# 1. FILE PATH
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Three_Mandals_NDVI_Clipped_20261009.tif"
)


# ============================================================
# 2. CHECK FILE
# ============================================================

if not RASTER_PATH.exists():
    raise FileNotFoundError(
        f"Clipped NDVI raster not found:\n{RASTER_PATH}"
    )


# ============================================================
# 3. READ RASTER AND CALCULATE STATISTICS
# ============================================================

with rasterio.open(RASTER_PATH) as src:

    ndvi = src.read(1, masked=True)

    # Convert to a NumPy masked array.
    values = np.ma.asarray(ndvi)

    # Valid pixels exclude NoData and non-finite values.
    valid_mask = (
        ~np.ma.getmaskarray(values)
        & np.isfinite(values.data)
    )

    valid_values = values.data[valid_mask]

    total_pixels = src.width * src.height
    valid_pixels = int(valid_mask.sum())
    nodata_pixels = total_pixels - valid_pixels

    valid_percentage = (
        valid_pixels / total_pixels * 100
        if total_pixels > 0
        else 0
    )

    print("\n" + "=" * 55)
    print("THREE-MANDAL NDVI VERIFICATION")
    print("=" * 55)

    print(f"File: {RASTER_PATH.name}")
    print(f"CRS: {src.crs}")
    print(f"Dimensions: {src.width} x {src.height}")
    print(f"Pixel size: {src.res}")
    print(f"NoData value: {src.nodata}")

    print("\n--- PIXEL COUNTS ---")
    print(f"Total pixels: {total_pixels:,}")
    print(f"Valid NDVI pixels: {valid_pixels:,}")
    print(f"NoData / invalid pixels: {nodata_pixels:,}")
    print(f"Valid pixel percentage: {valid_percentage:.2f}%")

    if valid_pixels > 0:
        print("\n--- NDVI STATISTICS ---")
        print(f"Minimum NDVI: {valid_values.min():.4f}")
        print(f"Maximum NDVI: {valid_values.max():.4f}")
        print(f"Mean NDVI: {valid_values.mean():.4f}")
        print(f"Median NDVI: {np.median(valid_values):.4f}")
        print(f"Standard deviation: {valid_values.std():.4f}")

        # Basic NDVI range check.
        outside_range = (
            (valid_values < -1.0) | (valid_values > 1.0)
        ).sum()

        print(f"Values outside [-1, 1]: {outside_range:,}")

    else:
        print("\nWARNING: No valid NDVI pixels were found.")

print("\nVerification complete.")
