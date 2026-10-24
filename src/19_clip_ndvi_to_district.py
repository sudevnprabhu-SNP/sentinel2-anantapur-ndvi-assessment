
from pathlib import Path

import geopandas as gpd
import rasterio
from rasterio.mask import mask

# Project root
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Input files
BOUNDARY_FILE = (
    PROJECT_DIR / "data" / "raw"
    / "district_nwic_geojson" / "district_nwic.GeoJSON"
)

NDVI_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "Anantapur_NDVI_Masked_20261009.tif"
)

# Output file
OUTPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "Anantapur_NDVI_District_Clipped_20261009.tif"
)

print("Loading Anantapur district boundary...")

# Read the national district boundary dataset
districts = gpd.read_file(BOUNDARY_FILE)

# Select Anantapur, Andhra Pradesh
anantapur = districts[
    (districts["district"].str.strip().str.casefold() == "anantapur")
    & (districts["state_name"].str.strip().str.casefold() == "andhra pradesh")
]

if anantapur.empty:
    raise ValueError("Anantapur, Andhra Pradesh was not found.")

print("District feature(s) found:", len(anantapur))

# Open the masked NDVI raster
with rasterio.open(NDVI_FILE) as src:
    print("Raster CRS:", src.crs)
    print("Boundary CRS:", anantapur.crs)

    if anantapur.crs is None:
        raise ValueError("The district boundary has no CRS defined.")

    # Reproject the boundary to the raster CRS
    anantapur = anantapur.to_crs(src.crs)

    # Clip raster to the district polygon
    clipped_data, clipped_transform = mask(
        src,
        anantapur.geometry,
        crop=True,
        nodata=src.nodata,
        filled=True
    )

    # Preserve raster metadata and update dimensions/transform
    output_metadata = src.meta.copy()
    output_metadata.update({
        "height": clipped_data.shape[1],
        "width": clipped_data.shape[2],
        "transform": clipped_transform,
        "nodata": src.nodata,
        "compress": "lzw"
    })

    # Save the new district-clipped raster
    with rasterio.open(OUTPUT_FILE, "w", **output_metadata) as dst:
        dst.write(clipped_data)

print("\nDistrict clipping completed!")
print("Output:", OUTPUT_FILE)
print("Output file exists:", OUTPUT_FILE.exists())
print("Output size:", clipped_data.shape[2], "x", clipped_data.shape[1])
print("Pixel size: 10 metres (inherited from the source raster)")
