
from pathlib import Path

import rasterio


PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
NDVI_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_20261009.tif"
)

scl_files = list(RAW_DIR.rglob("*SCL_20m.jp2"))

if not scl_files:
    raise FileNotFoundError("No SCL raster found.")

SCL_PATH = scl_files[0]


def show_raster_info(label, path):
    with rasterio.open(path) as src:
        print(f"\n--- {label} ---")
        print(f"File: {path}")
        print(f"CRS: {src.crs}")
        print(f"Dimensions: {src.width} x {src.height}")
        print(f"Pixel size: {src.res}")
        print(f"Bounds: {src.bounds}")
        print(f"Transform: {src.transform}")


show_raster_info("NDVI RASTER", NDVI_PATH)
show_raster_info("SCL RASTER", SCL_PATH)
