
from pathlib import Path
import geopandas as gpd
import rasterio
from shapely.geometry import box

PROJECT_DIR = Path(__file__).resolve().parent.parent

BOUNDARY_FILE = (
    PROJECT_DIR / "data" / "raw"
    / "district_nwic_geojson" / "district_nwic.GeoJSON"
)

RASTER_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "Anantapur_NDVI_District_Clipped_20261009.tif"
)

districts = gpd.read_file(BOUNDARY_FILE)

district = districts[
    (districts["district"].str.strip().str.casefold() == "anantapur")
    & (districts["state_name"].str.strip().str.casefold() == "andhra pradesh")
]

if district.empty:
    raise ValueError("Anantapur district was not found.")

with rasterio.open(RASTER_FILE) as src:
    district = district.to_crs(src.crs)
    raster_bounds = box(*src.bounds)
    district_geometry = district.geometry.union_all()

    print("--- DISTRICT / RASTER OVERLAP CHECK ---")
    print("Raster CRS:", src.crs)
    print("Raster bounds:", src.bounds)
    print("District bounds:", district.total_bounds)
    print("District geometry type:", district_geometry.geom_type)
    print("District area (square metres):", round(district_geometry.area, 2))
    print("Raster covers district bounds:",
          raster_bounds.covers(box(*district.total_bounds)))
    print("District intersects raster:", district_geometry.intersects(raster_bounds))
    print("District completely covered by raster:",
          raster_bounds.covers(district_geometry))
    print("Intersection area (square metres):",
          round(district_geometry.intersection(raster_bounds).area, 2))
