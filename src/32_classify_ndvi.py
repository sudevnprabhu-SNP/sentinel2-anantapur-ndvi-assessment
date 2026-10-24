
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.colors import BoundaryNorm, ListedColormap
from rasterio.plot import plotting_extent

# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]

INPUT_RASTER = (
    PROJECT_DIR / "data" / "processed"
    / "Three_Mandals_NDVI_Clipped_20261009.tif"
)

OUTPUT_RASTER = (
    PROJECT_DIR / "data" / "processed"
    / "Three_Mandals_NDVI_Classes_20261009.tif"
)

OUTPUT_MAP = (
    PROJECT_DIR / "reports"
    / "three_mandals_ndvi_classification.png"
)

OUTPUT_MAP.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Define NDVI classes
# --------------------------------------------------

# Class 1: NDVI < 0.00
# Class 2: NDVI 0.00 to < 0.15
# Class 3: NDVI 0.15 to < 0.30
# Class 4: NDVI 0.30 to < 0.45
# Class 5: NDVI >= 0.45

CLASS_NAMES = [
    "Below 0.00",
    "0.00 to < 0.15",
    "0.15 to < 0.30",
    "0.30 to < 0.45",
    "0.45 and above",
]

CLASS_COLORS = [
    "#2166AC",
    "#D9D9D9",
    "#FEE08B",
    "#91CF60",
    "#1A9850",
]

# --------------------------------------------------
# 3. Read NDVI and classify valid pixels
# --------------------------------------------------

print("Reading NDVI raster...")

with rasterio.open(INPUT_RASTER) as src:
    ndvi = src.read(1, masked=True)
    profile = src.profile.copy()
    extent = plotting_extent(src)
    raster_crs = src.crs

    ndvi_values = np.ma.getdata(ndvi)
    invalid = np.ma.getmaskarray(ndvi) | ~np.isfinite(ndvi_values)

    # Use 0 as the output NoData value.
    # Valid class codes are 1 through 5.
    classified = np.zeros(ndvi_values.shape, dtype=np.uint8)

    valid = ~invalid

    classified[valid & (ndvi_values < 0.00)] = 1
    classified[valid & (ndvi_values >= 0.00) &
               (ndvi_values < 0.15)] = 2
    classified[valid & (ndvi_values >= 0.15) &
               (ndvi_values < 0.30)] = 3
    classified[valid & (ndvi_values >= 0.30) &
               (ndvi_values < 0.45)] = 4
    classified[valid & (ndvi_values >= 0.45)] = 5

# --------------------------------------------------
# 4. Save classified GeoTIFF
# --------------------------------------------------

profile.update(
    dtype=rasterio.uint8,
    count=1,
    nodata=0,
    compress="lzw",
)

with rasterio.open(OUTPUT_RASTER, "w", **profile) as dst:
    dst.write(classified, 1)

print(f"CRS: {raster_crs}")
print(f"Classified raster saved to: {OUTPUT_RASTER}")

# --------------------------------------------------
# 5. Calculate class statistics
# --------------------------------------------------

print("\n" + "=" * 60)
print("NDVI CLASS DISTRIBUTION")
print("=" * 60)

valid_classified = classified > 0
total_valid = int(valid_classified.sum())

class_counts = []

for class_code, class_name in enumerate(CLASS_NAMES, start=1):
    count = int((classified == class_code).sum())
    percentage = (
        count / total_valid * 100 if total_valid > 0 else 0
    )

    class_counts.append(count)

    print(
        f"Class {class_code}: {class_name:<18} "
        f"{count:>10,} pixels  ({percentage:>6.2f}%)"
    )

print(f"\nTotal valid pixels: {total_valid:,}")
print(f"NoData pixels: {int((~valid_classified).sum()):,}")

# --------------------------------------------------
# 6. Create classification map
# --------------------------------------------------

print("\nCreating classification map...")

cmap = ListedColormap(CLASS_COLORS)
cmap.set_bad("white")

# Mask NoData class 0 so it appears white
display_data = np.ma.masked_equal(classified, 0)

fig, ax = plt.subplots(figsize=(10, 10))

image = ax.imshow(
    display_data,
    extent=extent,
    origin="upper",
    cmap=cmap,
    norm=BoundaryNorm(
        np.arange(0.5, 6.5, 1),
        cmap.N,
    ),
    interpolation="nearest",
)

colorbar = fig.colorbar(
    image,
    ax=ax,
    ticks=[1, 2, 3, 4, 5],
    shrink=0.75,
    pad=0.03,
)

colorbar.ax.set_yticklabels(CLASS_NAMES)
colorbar.set_label("NDVI class", fontsize=10)

ax.set_title(
    "NDVI Classification\n"
    "Anantapur Urban, Anantapur Rural & Bukkaraya Samudram\n"
    "Sentinel-2 | 9 October 2026",
    fontsize=13,
    pad=14,
)

ax.set_xlabel("Easting (m)")
ax.set_ylabel("Northing (m)")
ax.set_aspect("equal")

ax.ticklabel_format(
    style="plain",
    axis="both",
    useOffset=False,
)

ax.grid(
    visible=True,
    linestyle="--",
    linewidth=0.4,
    alpha=0.35,
)

fig.tight_layout()
fig.savefig(OUTPUT_MAP, dpi=300, bbox_inches="tight")
plt.close(fig)

print(f"Classification map saved to: {OUTPUT_MAP}")
print("\nNDVI classification complete.")
