
from pathlib import Path

import numpy as np
import rasterio


PROJECT_DIR = Path(__file__).resolve().parent.parent

NDVI_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_20261009.tif"
)

MASK_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_SCL_CloudMask_20261009.tif"
)

OUTPUT_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_Masked_20261009.tif"
)

# Use a floating-point NoData marker outside the normal NDVI range.
NODATA_VALUE = -9999.0

with rasterio.open(NDVI_PATH) as ndvi_src, \
     rasterio.open(MASK_PATH) as mask_src:

    ndvi = ndvi_src.read(1).astype(np.float32)
    mask = mask_src.read(1)

    if ndvi.shape != mask.shape:
        raise ValueError("NDVI and mask dimensions do not match.")

    if ndvi_src.transform != mask_src.transform:
        raise ValueError("NDVI and mask grids do not match.")

    if ndvi_src.crs != mask_src.crs:
        raise ValueError("NDVI and mask CRS do not match.")

    profile = ndvi_src.profile.copy()

# Exclude masked pixels and any non-finite NDVI values.
valid = (mask == 0) & np.isfinite(ndvi)

cleaned = np.full(ndvi.shape, NODATA_VALUE, dtype=np.float32)
cleaned[valid] = ndvi[valid]

profile.update(
    driver="GTiff",
    dtype="float32",
    count=1,
    nodata=NODATA_VALUE,
    compress="lzw",
)

with rasterio.open(OUTPUT_PATH, "w", **profile) as dst:
    dst.write(cleaned, 1)

print("--- MASKED NDVI CREATED ---")
print(f"Output: {OUTPUT_PATH}")
print(f"Valid NDVI pixels: {np.count_nonzero(valid):,}")
print(f"Excluded pixels: {np.count_nonzero(~valid):,}")
print(f"NoData value: {NODATA_VALUE}")
print("Original NDVI raster was not modified.")
