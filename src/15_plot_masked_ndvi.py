
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio


PROJECT_DIR = Path(__file__).resolve().parent.parent

RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_Masked_20261009.tif"
)

OUTPUT_DIR = PROJECT_DIR / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # Read the masked NDVI raster
    with rasterio.open(RASTER_PATH) as dataset:
        ndvi = dataset.read(1, masked=True)

    # Remove NoData and any non-finite values
    values = ndvi.compressed()
    values = values[np.isfinite(values)]

    if values.size == 0:
        print("No valid NDVI pixels found.")
        return

    # Sample pixels to keep plotting memory-efficient
    rng = np.random.default_rng(42)
    sample_size = min(500_000, values.size)

    if values.size > sample_size:
        values = rng.choice(
            values,
            size=sample_size,
            replace=False
        )

    # Plot the distribution
    plt.figure(figsize=(10, 6))

    plt.hist(
        values,
        bins=100,
        edgecolor="black",
        linewidth=0.2
    )

    plt.title("Masked NDVI Distribution - Anantapur")
    plt.xlabel("NDVI value")
    plt.ylabel("Number of sampled pixels")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "masked_ndvi_distribution.png"
    plt.savefig(output_path, dpi=300)
    plt.show()
    plt.close()

    print(f"Sampled pixels plotted: {sample_size:,}")
    print(f"Histogram saved to: {output_path}")


if __name__ == "__main__":
    main()
