
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.enums import Resampling


PROJECT_DIR = Path(__file__).resolve().parent.parent

RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_Masked_20261009.tif"
)

OUTPUT_PATH = PROJECT_DIR / "reports" / "masked_ndvi_preview.png"

with rasterio.open(RASTER_PATH) as src:
    ndvi = src.read(
        1,
        out_shape=(600, 600),
        masked=True,
        resampling=Resampling.nearest,
    )

values = ndvi.compressed()
values = values[np.isfinite(values)]

print("--- MASKED NDVI PREVIEW ---")
print(f"Preview dimensions: {ndvi.shape}")
print(f"Valid preview pixels: {values.size:,}")

plt.figure(figsize=(10, 7))
image = plt.imshow(ndvi, cmap="RdYlGn", vmin=0, vmax=0.6)
plt.title("Anantapur NDVI After SCL Masking")
plt.xlabel("Column")
plt.ylabel("Row")
plt.colorbar(image, label="NDVI")
plt.tight_layout()

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=200)
plt.show()
plt.close()

print(f"Preview saved to: {OUTPUT_PATH}")
