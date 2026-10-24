
from pathlib import Path

import numpy as np
import rasterio


PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"

scl_files = list(RAW_DIR.rglob("*SCL_20m.jp2"))

if not scl_files:
    raise FileNotFoundError("No Sentinel-2 SCL file found.")

SCL_PATH = scl_files[0]

print("--- SCL RASTER INSPECTION ---")
print(f"File: {SCL_PATH}")

with rasterio.open(SCL_PATH) as dataset:
    print(f"Width: {dataset.width} pixels")
    print(f"Height: {dataset.height} pixels")
    print(f"Coordinate system: {dataset.crs}")
    print(f"Pixel size: {dataset.res}")
    print(f"Data type: {dataset.dtypes[0]}")

    scl = dataset.read(1)
    classes, counts = np.unique(scl, return_counts=True)

print("\n--- SCL CLASS COUNTS ---")

for class_value, count in zip(classes, counts):
    print(f"Class {class_value}: {count:,} pixels")
