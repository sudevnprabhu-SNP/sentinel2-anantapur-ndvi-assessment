
from pathlib import Path

import rasterio

# Path to the processed Sentinel-2 NDVI raster
PROJECT_DIR = Path(__file__).resolve().parent.parent
RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_20261009.tif"
)


def main():
    if not RASTER_PATH.exists():
        print("ERROR: NDVI raster was not found.")
        print(f"Expected location: {RASTER_PATH}")
        return

    with rasterio.open(RASTER_PATH) as dataset:
        print("\n--- SENTINEL-2 NDVI RASTER INSPECTION ---")
        print(f"File: {dataset.name}")
        print(f"Width: {dataset.width} pixels")
        print(f"Height: {dataset.height} pixels")
        print(f"Number of bands: {dataset.count}")
        print(f"Coordinate system: {dataset.crs}")
        print(f"Pixel size: {dataset.res}")
        print(f"Data type: {dataset.dtypes[0]}")
        print(f"NoData value: {dataset.nodata}")
        print(f"Bounds: {dataset.bounds}")

    print("\nRaster inspection completed.")


if __name__ == "__main__":
    main()
