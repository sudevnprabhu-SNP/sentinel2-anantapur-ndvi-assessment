
from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject


PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
NDVI_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_20261009.tif"
)
OUTPUT_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_SCL_CloudMask_20261009.tif"
)

scl_files = list(RAW_DIR.rglob("*SCL_20m.jp2"))

if not scl_files:
    raise FileNotFoundError("No SCL raster found.")

SCL_PATH = scl_files[0]

# SCL classes excluded in the initial mask.
EXCLUDED_CLASSES = [0, 1, 3, 7, 8, 9, 10]

with rasterio.open(NDVI_PATH) as ndvi_src:
    target_profile = ndvi_src.profile.copy()
    target_shape = (ndvi_src.height, ndvi_src.width)
    target_transform = ndvi_src.transform
    target_crs = ndvi_src.crs

with rasterio.open(SCL_PATH) as scl_src:
    scl_aligned = np.zeros(target_shape, dtype=np.uint8)

    reproject(
        source=rasterio.band(scl_src, 1),
        destination=scl_aligned,
        src_transform=scl_src.transform,
        src_crs=scl_src.crs,
        dst_transform=target_transform,
        dst_crs=target_crs,
        resampling=Resampling.nearest,
    )

# 1 = excluded; 0 = retained
mask = np.isin(scl_aligned, EXCLUDED_CLASSES).astype(np.uint8)

target_profile.update(
    driver="GTiff",
    count=1,
    dtype="uint8",
    nodata=None,
    compress="lzw",
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

with rasterio.open(OUTPUT_PATH, "w", **target_profile) as dst:
    dst.write(mask, 1)

values, counts = np.unique(mask, return_counts=True)

print("--- CLOUD MASK CREATED ---")
print(f"Output: {OUTPUT_PATH}")
print(f"Dimensions: {target_shape[1]} x {target_shape[0]}")

for value, count in zip(values, counts):
    label = "Excluded" if value == 1 else "Retained"
    print(f"{label} pixels: {count:,}")

print("Mask values: 1 = excluded; 0 = retained")
