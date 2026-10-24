
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.plot import plotting_extent
from matplotlib.colors import Normalize


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_Masked_20261009.tif"
)

OUTPUT_DIR = PROJECT_DIR / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = OUTPUT_DIR / "masked_ndvi_map.png"


# --------------------------------------------------
# 2. Read the masked NDVI raster
# --------------------------------------------------

def main():
    print("Loading masked NDVI raster...")

    with rasterio.open(RASTER_PATH) as dataset:
        ndvi = dataset.read(1, masked=True)
        extent = plotting_extent(dataset)
        crs = dataset.crs
        pixel_size = dataset.res
        nodata = dataset.nodata

    # Exclude NoData and non-finite pixels
    values = ndvi.compressed()
    values = values[np.isfinite(values)]

    if values.size == 0:
        print("No valid NDVI pixels found.")
        return

    print(f"CRS: {crs}")
    print(f"Pixel size: {pixel_size}")
    print(f"NoData value: {nodata}")
    print(f"Valid pixels: {values.size:,}")
    print(f"Minimum NDVI: {values.min():.4f}")
    print(f"Maximum NDVI: {values.max():.4f}")
    print(f"Mean NDVI: {values.mean():.4f}")

    # --------------------------------------------------
    # 3. Plot the spatial NDVI map
    # --------------------------------------------------

    print("Creating map...")

    fig, ax = plt.subplots(figsize=(10, 10))

    image = ax.imshow(
        ndvi,
        extent=extent,
        origin="upper",
        cmap="RdYlGn",
        norm=Normalize(vmin=-0.2, vmax=0.7),
        interpolation="nearest"
    )

    colorbar = fig.colorbar(
        image,
        ax=ax,
        shrink=0.75,
        pad=0.03
    )

    colorbar.set_label("NDVI", fontsize=11)

    ax.set_title(
        "Sentinel-2 Masked NDVI Map\n"
        "Acquisition date: 9 October 2026",
        fontsize=14,
        pad=14
    )

    ax.set_xlabel("Easting (m)")
    ax.set_ylabel("Northing (m)")
    ax.set_aspect("equal")

    ax.ticklabel_format(
        style="plain",
        axis="both",
        useOffset=False
    )

    fig.text(
        0.5,
        0.02,
        "White/transparent areas: NoData or masked pixels. "
        "Study area covers the raster footprint, not a district boundary.",
        ha="center",
        fontsize=8,
        wrap=True
    )

    plt.tight_layout(rect=[0, 0.05, 1, 1])

    # --------------------------------------------------
    # 4. Save the map
    # --------------------------------------------------

    fig.savefig(
        OUTPUT_PATH,
        dpi=300,
        bbox_inches="tight",
        facecolor="white"
    )

    print(f"Map saved to: {OUTPUT_PATH}")

    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
