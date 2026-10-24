
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.enums import Resampling


PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"

scl_files = list(RAW_DIR.rglob("*SCL_20m.jp2"))

if not scl_files:
    raise FileNotFoundError("No SCL raster found.")

SCL_PATH = scl_files[0]

with rasterio.open(SCL_PATH) as src:
    # Read a smaller version for visualization.
    scl_small = src.read(
        1,
        out_shape=(600, 600),
        resampling=Resampling.nearest,
    )

# Show where Class 0 occurs.
class_zero = scl_small == 0

print("--- SCL SPATIAL CHECK ---")
print(f"Preview dimensions: {scl_small.shape}")
print(
    "Class 0 percentage in preview: "
    f"{class_zero.mean() * 100:.2f}%"
)

plt.figure(figsize=(9, 7))
plt.imshow(class_zero, interpolation="nearest")
plt.title("Sentinel-2 SCL: Locations of Class 0")
plt.xlabel("Column")
plt.ylabel("Row")
plt.tight_layout()

output_path = PROJECT_DIR / "reports" / "scl_class0_preview.png"
output_path.parent.mkdir(parents=True, exist_ok=True)
plt.savefig(output_path, dpi=200)
plt.show()
plt.close()

print(f"Preview saved to: {output_path}")
