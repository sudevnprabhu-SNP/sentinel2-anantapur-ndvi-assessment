
from pathlib import Path

import numpy as np
import rasterio


PROJECT_DIR = Path(__file__).resolve().parent.parent

RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_Masked_20261009.tif"
)


def main():
    with rasterio.open(RASTER_PATH) as src:
        print("--- MASKED NDVI VERIFICATION ---")
        print(f"Raster size: {src.width} x {src.height}")
        print(f"NoData value: {src.nodata}")
        print(f"Data type: {src.dtypes[0]}")

        valid_pixels = 0
        nodata_pixels = 0
        other_invalid_pixels = 0
        ndvi_sum = 0.0
        ndvi_min = float("inf")
        ndvi_max = float("-inf")

        for _, window in src.block_windows(1):
            data = src.read(1, window=window)

            nodata_mask = data == src.nodata
            finite_mask = np.isfinite(data)
            valid_mask = finite_mask & ~nodata_mask

            valid = data[valid_mask]

            valid_pixels += valid.size
            nodata_pixels += np.count_nonzero(nodata_mask)
            other_invalid_pixels += np.count_nonzero(
                ~finite_mask & ~nodata_mask
            )

            if valid.size:
                ndvi_sum += valid.astype(np.float64).sum()
                ndvi_min = min(ndvi_min, float(valid.min()))
                ndvi_max = max(ndvi_max, float(valid.max()))

        total_pixels = src.width * src.height

        print(f"Total pixels: {total_pixels:,}")
        print(f"Valid pixels: {valid_pixels:,}")
        print(f"NoData pixels: {nodata_pixels:,}")
        print(f"Other non-finite pixels: {other_invalid_pixels:,}")
        print(f"Valid percentage: {100 * valid_pixels / total_pixels:.2f}%")

        if valid_pixels:
            print(f"Mean NDVI: {ndvi_sum / valid_pixels:.4f}")
            print(f"Minimum NDVI: {ndvi_min:.4f}")
            print(f"Maximum NDVI: {ndvi_max:.4f}")


if __name__ == "__main__":
    main()
