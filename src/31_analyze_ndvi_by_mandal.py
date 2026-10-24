
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import geometry_mask

# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]

RASTER_PATH = (
    PROJECT_DIR / "data" / "processed"
    / "Three_Mandals_NDVI_Clipped_20261009.tif"
)

BOUNDARY_PATH = (
    PROJECT_DIR / "data" / "processed"
    / "Three_Mandals_Study_Area.geojson"
)

REPORTS_DIR = PROJECT_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = REPORTS_DIR / "ndvi_statistics_by_mandal.csv"
CHART_PATH = REPORTS_DIR / "mean_ndvi_by_mandal.png"


# --------------------------------------------------
# 2. Read boundaries and raster
# --------------------------------------------------

print("Reading study-area boundaries and NDVI raster...")

boundaries = gpd.read_file(BOUNDARY_PATH)

results = []

with rasterio.open(RASTER_PATH) as src:
    ndvi = src.read(1, masked=True)
    raster_crs = src.crs
    transform = src.transform
    raster_shape = (src.height, src.width)

    boundaries = boundaries.to_crs(raster_crs)

    ndvi_data = np.ma.getdata(ndvi)
    invalid_mask = np.ma.getmaskarray(ndvi)
    valid_mask = ~invalid_mask & np.isfinite(ndvi_data)

    # --------------------------------------------------
    # 3. Calculate statistics for each mandal
    # --------------------------------------------------

    for _, mandal in boundaries.iterrows():
        name = mandal["mandal_name"]
        geometry = mandal.geometry

        inside = geometry_mask(
            [geometry],
            out_shape=raster_shape,
            transform=transform,
            invert=True,
            all_touched=False,
        )

        valid_pixels = inside & valid_mask
        values = ndvi_data[valid_pixels]

        total_pixels = int(inside.sum())
        valid_count = int(len(values))
        invalid_count = total_pixels - valid_count

        if valid_count == 0:
            print(f"WARNING: No valid NDVI pixels for {name}")
            continue

        results.append({
            "Mandal": name,
            "Total_Pixels": total_pixels,
            "Valid_Pixels": valid_count,
            "Invalid_Pixels": invalid_count,
            "Valid_Coverage_Percent": (
                valid_count / total_pixels * 100
                if total_pixels else np.nan
            ),
            "Mean_NDVI": float(np.mean(values)),
            "Median_NDVI": float(np.median(values)),
            "Minimum_NDVI": float(np.min(values)),
            "Maximum_NDVI": float(np.max(values)),
            "Standard_Deviation": float(np.std(values)),
        })

# --------------------------------------------------
# 4. Save statistics to CSV
# --------------------------------------------------

df = pd.DataFrame(results)

df.to_csv(CSV_PATH, index=False, float_format="%.5f")

print("\n" + "=" * 65)
print("NDVI STATISTICS BY MANDAL")
print("=" * 65)

if not df.empty:
    print(df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print(f"\nCSV saved to: {CSV_PATH}")

    # --------------------------------------------------
    # 5. Plot mean NDVI
    # --------------------------------------------------

    fig, ax = plt.subplots(figsize=(9, 5.5))

    bars = ax.bar(
        df["Mandal"],
        df["Mean_NDVI"],
    )

    ax.bar_label(
        bars,
        fmt="%.3f",
        padding=4,
    )

    ax.set_title(
        "Mean NDVI by Mandal\nSentinel-2, 9 October 2026",
        fontsize=13,
    )
    ax.set_xlabel("Mandal")
    ax.set_ylabel("Mean NDVI")
    ax.set_ylim(0, max(0.1, float(df["Mean_NDVI"].max()) * 1.2))
    ax.tick_params(axis="x", rotation=15)
    ax.grid(axis="y", linestyle="--", alpha=0.35)

    fig.tight_layout()
    fig.savefig(CHART_PATH, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Mean NDVI chart saved to: {CHART_PATH}")

print("\nMandal-wise analysis complete.")
