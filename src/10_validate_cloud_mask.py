
from pathlib import Path

import numpy as np
import rasterio


PROJECT_DIR = Path(__file__).resolve().parent.parent

MASK_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_SCL_CloudMask_20261009.tif"
)

NDVI_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_20261009.tif"
)

with rasterio.open(MASK_PATH) as mask_src, \
     rasterio.open(NDVI_PATH) as ndvi_src:

    mask = mask_src.read(1)

    print("--- MASK VALIDATION ---")
    print(f"Mask dimensions: {mask_src.width} x {mask_src.height}")
    print(f"NDVI dimensions: {ndvi_src.width} x {ndvi_src.height}")
    print(f"Same CRS: {mask_src.crs == ndvi_src.crs}")
    print(f"Same bounds: {mask_src.bounds == ndvi_src.bounds}")
    print(f"Same transform: {mask_src.transform == ndvi_src.transform}")

    values, counts = np.unique(mask, return_counts=True)
    print(f"Mask values found: {values.tolist()}")

    for value, count in zip(values, counts):
        print(f"Value {value}: {count:,} pixels")

    print(f"Unexpected values: {np.count_nonzero(~np.isin(mask, [0, 1])):,}")

print("Validation completed.")
