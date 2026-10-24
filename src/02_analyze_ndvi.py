
from pathlib import Path

import numpy as np
import rasterio


PROJECT_DIR = Path(__file__).resolve().parent.parent
RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_20261009.tif"
)


def main():
    with rasterio.open(RASTER_PATH) as dataset:
        ndvi = dataset.read(1, masked=True)

    # Exclude masked pixels and any non-finite values
    values = np.asarray(ndvi.compressed())
    values = values[np.isfinite(values)]

    if values.size == 0:
        print("No valid NDVI pixels found.")
        return

    print("\n--- NDVI STATISTICAL ANALYSIS ---")
    print(f"Valid pixels: {values.size:,}")
    print(f"Minimum NDVI: {values.min():.4f}")
    print(f"Maximum NDVI: {values.max():.4f}")
    print(f"Mean NDVI: {values.mean():.4f}")
    print(f"Median NDVI: {np.median(values):.4f}")
    print(f"Standard deviation: {values.std():.4f}")

    print("\n--- NDVI PERCENTILES ---")
    for percentile in [5, 25, 50, 75, 95]:
        result = np.percentile(values, percentile)
        print(f"{percentile}th percentile: {result:.4f}")


if __name__ == "__main__":
    main()
