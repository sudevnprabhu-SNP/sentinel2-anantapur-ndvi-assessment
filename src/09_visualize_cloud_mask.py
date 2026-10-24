
from pathlib import Path

import matplotlib.pyplot as plt
import rasterio
from rasterio.enums import Resampling


PROJECT_DIR = Path(__file__).resolve().parent.parent

MASK_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_SCL_CloudMask_20261009.tif"
)

OUTPUT_PATH = (
    PROJECT_DIR
    / "reports"
    / "cloud_mask_preview.png"
)

with rasterio.open(MASK_PATH) as src:
    mask = src.read(
        1,
        out_shape=(600, 600),
        resampling=Resampling.nearest,
    )

plt.figure(figsize=(9, 7))
plt.imshow(mask, cmap="gray", vmin=0, vmax=1)
plt.title("Sentinel-2 Cloud and Invalid-Pixel Mask")
plt.xlabel("Column")
plt.ylabel("Row")
plt.colorbar(
    label="Mask value (0 = retained, 1 = excluded)",
    ticks=[0, 1],
)
plt.tight_layout()

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(OUTPUT_PATH, dpi=200)
plt.show()
plt.close()

print(f"Mask preview saved to: {OUTPUT_PATH}")
