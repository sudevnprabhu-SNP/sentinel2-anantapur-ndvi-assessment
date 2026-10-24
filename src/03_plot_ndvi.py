
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio


PROJECT_DIR = Path(__file__).resolve().parent.parent
RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_20261009.tif"
)
OUTPUT_DIR = PROJECT_DIR / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    with rasterio.open(RASTER_PATH) as dataset:
        ndvi = dataset.read(1, masked=True)

    values = ndvi.compressed()
    values = values[np.isfinite(values)]

    if values.size == 0:
        print("No valid NDVI pixels found.")
        return

    # Histogram: show how frequently NDVI values occur
    plt.figure(figsize=(10, 6))
    plt.hist(values, bins=100, edgecolor="black", linewidth=0.2)
    plt.title("NDVI Distribution - Anantapur")
    plt.xlabel("NDVI value")
    plt.ylabel("Number of pixels")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "ndvi_distribution.png"
    plt.savefig(output_path, dpi=300)
    plt.show()
    plt.close()

    print(f"Histogram saved to: {output_path}")


if __name__ == "__main__":
    main()
