
from pathlib import Path

import numpy as np
import rasterio


PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

FILES = {
    "Original NDVI": (
        PROCESSED_DIR / "Anantapur_NDVI_20261009.tif"
    ),
    "Masked NDVI": (
        PROCESSED_DIR / "Anantapur_NDVI_Masked_20261009.tif"
    ),
}


def calculate_statistics(path):
    with rasterio.open(path) as src:
        data = src.read(1, masked=True).astype(np.float32)

    values = data.compressed()
    values = values[np.isfinite(values)]

    if values.size == 0:
        raise ValueError(f"No valid pixels found in {path.name}")

    return {
        "valid_pixels": values.size,
        "mean": np.mean(values),
        "median": np.median(values),
        "std": np.std(values),
        "p5": np.percentile(values, 5),
        "p25": np.percentile(values, 25),
        "p75": np.percentile(values, 75),
        "p95": np.percentile(values, 95),
    }


results = {}

for label, path in FILES.items():
    if not path.exists():
        raise FileNotFoundError(path)

    results[label] = calculate_statistics(path)

print("--- ORIGINAL VS MASKED NDVI ---")

for label, stats in results.items():
    print(f"\n{label}")
    print(f"Valid pixels: {stats['valid_pixels']:,}")
    print(f"Mean: {stats['mean']:.4f}")
    print(f"Median: {stats['median']:.4f}")
    print(f"Standard deviation: {stats['std']:.4f}")
    print(f"5th percentile: {stats['p5']:.4f}")
    print(f"25th percentile: {stats['p25']:.4f}")
    print(f"75th percentile: {stats['p75']:.4f}")
    print(f"95th percentile: {stats['p95']:.4f}")

print("\n--- CHANGE AFTER MASKING ---")

original = results["Original NDVI"]
masked = results["Masked NDVI"]

for metric in ["mean", "median", "std", "p5", "p25", "p75", "p95"]:
    difference = masked[metric] - original[metric]
    print(f"{metric}: {difference:+.4f}")
