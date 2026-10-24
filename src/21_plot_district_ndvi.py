
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio

PROJECT_DIR = Path(__file__).resolve().parent.parent

RASTER_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "Anantapur_NDVI_District_Clipped_20261009.tif"
)

OUTPUT_FILE = (
    PROJECT_DIR / "reports"
    / "anantapur_district_ndvi_map.png"
)

with rasterio.open(RASTER_FILE) as src:
    ndvi = src.read(1, masked=True)
    bounds = src.bounds

print("Creating Anantapur district NDVI map...")
print("Raster dimensions:", ndvi.shape)
print("Valid pixels:", ndvi.count())

# Masked pixels are displayed transparently.
ndvi = np.ma.masked_invalid(ndvi)

fig, ax = plt.subplots(figsize=(10, 10))

image = ax.imshow(
    ndvi,
    cmap="RdYlGn",
    vmin=-1,
    vmax=1,
    extent=[
        bounds.left,
        bounds.right,
        bounds.bottom,
        bounds.top
    ],
    origin="upper"
)

colorbar = fig.colorbar(image, ax=ax, shrink=0.75)
colorbar.set_label("Normalized Difference Vegetation Index (NDVI)")

ax.set_title(
    "Sentinel-2 NDVI — Anantapur District\n"
    "Acquisition date: 9 October 2026"
)
ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")
ax.set_aspect("equal")

fig.tight_layout()
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
plt.close(fig)

print("Map saved to:", OUTPUT_FILE)
