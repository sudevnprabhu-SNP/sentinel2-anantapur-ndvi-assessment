
from pathlib import Path

import numpy as np
import rasterio

PROJECT_DIR = Path(__file__).resolve().parent.parent

RASTER_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "Anantapur_NDVI_District_Clipped_20261009.tif"
)

print("--- ANANTAPUR DISTRICT NDVI VERIFICATION ---")

with rasterio.open(RASTER_FILE) as src:
    data = src.read(1, masked=True)

    valid = data.compressed()
    total_pixels = src.width * src.height
    valid_pixels = valid.size
    nodata_pixels = total_pixels - valid_pixels

    print("File:", RASTER_FILE.name)
    print("CRS:", src.crs)
    print("Dimensions:", src.width, "x", src.height)
    print("Pixel size:", src.res)
    print("NoData value:", src.nodata)
    print("Total pixels:", total_pixels)
    print("Valid pixels:", valid_pixels)
    print("NoData pixels:", nodata_pixels)
    print(f"Valid pixel percentage: {100 * valid_pixels / total_pixels:.2f}%")

    if valid_pixels > 0:
        print(f"Minimum NDVI: {np.min(valid):.4f}")
        print(f"Maximum NDVI: {np.max(valid):.4f}")
        print(f"Mean NDVI: {np.mean(valid):.4f}")
        print(f"Median NDVI: {np.median(valid):.4f}")
        print(f"Standard deviation: {np.std(valid):.4f}")
    else:
        print("WARNING: No valid pixels found!")

print("\nVerification completed.")
