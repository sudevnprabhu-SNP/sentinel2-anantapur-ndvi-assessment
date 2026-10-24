
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.plot import plotting_extent

# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]

RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Three_Mandals_NDVI_Clipped_20261009.tif"
)

BOUNDARY_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Three_Mandals_Study_Area.geojson"
)

OUTPUT_PATH = (
    PROJECT_DIR
    / "reports"
    / "three_mandals_ndvi_map.png"
)

# Create reports folder if it does not exist
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Read NDVI raster and study-area boundaries
# --------------------------------------------------

print("Reading NDVI raster and study-area boundaries...")

boundaries = gpd.read_file(BOUNDARY_PATH)

with rasterio.open(RASTER_PATH) as src:
    ndvi = src.read(1, masked=True)
    raster_crs = src.crs
    extent = plotting_extent(src)

# Ensure boundaries use the same CRS as the raster
boundaries = boundaries.to_crs(raster_crs)

# Convert invalid pixels to NaN for plotting
ndvi_data = ndvi.astype("float32").filled(np.nan)

print(f"Raster CRS: {raster_crs}")
print(f"Number of boundary features: {len(boundaries)}")


# --------------------------------------------------
# 3. Create the NDVI map
# --------------------------------------------------

print("Creating map...")

fig, ax = plt.subplots(figsize=(10, 10))

image = ax.imshow(
    ndvi_data,
    extent=extent,
    origin="upper",
    cmap="RdYlGn",
    vmin=-1,
    vmax=1,
    interpolation="nearest",
)

# Draw the outlines of the three mandals
boundaries.boundary.plot(
    ax=ax,
    color="black",
    linewidth=1.2,
)

# Add NDVI colour scale
colorbar = fig.colorbar(
    image,
    ax=ax,
    shrink=0.75,
    pad=0.03,
)

colorbar.set_label("NDVI", fontsize=11)
colorbar.set_ticks([-1, -0.5, 0, 0.5, 1])

# Titles and axis labels
ax.set_title(
    "Sentinel-2 NDVI Map\n"
    "Anantapur Urban, Anantapur Rural & Bukkaraya Samudram\n"
    "Acquisition Date: 9 October 2026",
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

# --------------------------------------------------
# 4. Save the map
# --------------------------------------------------

fig.savefig(
    OUTPUT_PATH,
    dpi=300,
    bbox_inches="tight",
)

plt.close(fig)

print("\n" + "=" * 55)
print("NDVI MAP CREATED SUCCESSFULLY")
print("=" * 55)
print(f"Saved to: {OUTPUT_PATH}")
print("Resolution: 300 DPI")
print("Colour scale: -1 to +1")
print("Boundary outlines: Three-mandal study area")
