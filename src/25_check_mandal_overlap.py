
from pathlib import Path

import geopandas as gpd
import rasterio
from shapely.geometry import box


# ============================================================
# 1. PROJECT FILE PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

RASTER_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "Anantapur_NDVI_Masked_20261009.tif"
)

MANDAL_FILES = [
    (
        "Anantapur Urban and Rural",
        PROJECT_DIR
        / "data"
        / "processed"
        / "Anantapur_Urban_Rural_Bukkarayasamudram.geojson",
    ),
    (
        "Bukkaraya Samudram",
        PROJECT_DIR
        / "data"
        / "processed"
        / "Bukkaraya_Samudram.geojson",
    ),
]


# ============================================================
# 2. CHECK INPUT FILES
# ============================================================

if not RASTER_PATH.exists():
    raise FileNotFoundError(
        f"NDVI raster not found:\n{RASTER_PATH}"
    )

print("\nChecking input files...")

for label, path in MANDAL_FILES:
    if path.exists():
        print(f"Found {label}: {path.name}")
    else:
        print(f"WARNING: Missing {label} file: {path.name}")


# ============================================================
# 3. READ SENTINEL-2 RASTER FOOTPRINT
# ============================================================

with rasterio.open(RASTER_PATH) as raster:
    raster_crs = raster.crs
    raster_bounds = raster.bounds

    raster_geometry = box(
        raster_bounds.left,
        raster_bounds.bottom,
        raster_bounds.right,
        raster_bounds.top,
    )

print("\n" + "=" * 60)
print("SENTINEL-2 MANDAL COVERAGE CHECK")
print("=" * 60)

print(f"Raster file: {RASTER_PATH.name}")
print(f"Coordinate system: {raster_crs}")
print(f"Raster bounds: {raster_bounds}")


# ============================================================
# 4. LOAD AND COMBINE MANDAL BOUNDARIES
# ============================================================

boundary_layers = []

for label, path in MANDAL_FILES:
    if not path.exists():
        continue

    boundaries = gpd.read_file(path)

    if boundaries.empty:
        print(f"\nWARNING: No boundaries found in {path.name}")
        continue

    if "mandal_name" not in boundaries.columns:
        print(
            f"\nWARNING: 'mandal_name' field missing "
            f"from {path.name}"
        )
        continue

    boundaries = boundaries.to_crs(raster_crs)
    boundary_layers.append(boundaries)

if not boundary_layers:
    raise ValueError(
        "No usable mandal boundaries were loaded. "
        "Check your GeoJSON files and file paths."
    )

mandals = gpd.GeoDataFrame(
    gpd.pd.concat(boundary_layers, ignore_index=True),
    geometry="geometry",
    crs=raster_crs,
)

# Remove duplicate mandals if a boundary appears in both files.
mandals = mandals.drop_duplicates(
    subset=["mandal_name"]
).reset_index(drop=True)

print("\nMandal names found:", mandals["mandal_name"].tolist())


# ============================================================
# 5. CALCULATE FOOTPRINT COVERAGE FOR EACH MANDAL
# ============================================================

print("\n" + "-" * 60)

for _, mandal in mandals.iterrows():
    name = mandal["mandal_name"]
    geometry = mandal.geometry

    print(f"\nMandal: {name}")

    if geometry is None or geometry.is_empty:
        print("Result: Invalid or empty boundary.")
        continue

    if not geometry.is_valid:
        print("WARNING: Boundary geometry is invalid.")

    mandal_area = geometry.area

    if mandal_area <= 0:
        print("Result: Boundary has zero area.")
        continue

    intersection = geometry.intersection(raster_geometry)
    overlap_area = intersection.area

    coverage_percentage = (
        overlap_area / mandal_area
    ) * 100

    # Guard against tiny floating-point rounding differences.
    coverage_percentage = min(100.0, max(0.0, coverage_percentage))

    print(f"Total boundary area: {mandal_area / 1_000_000:.2f} km²")
    print(f"Area inside raster: {overlap_area / 1_000_000:.2f} km²")
    print(f"Footprint coverage: {coverage_percentage:.2f}%")

    if coverage_percentage >= 99.9:
        print("Result: Almost completely covered.")
    elif coverage_percentage > 0:
        print("Result: Partially covered.")
    else:
        print("Result: Outside the raster footprint.")


# ============================================================
# 6. SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("COVERAGE CHECK COMPLETE")
print("=" * 60)

print("This checks geographic footprint coverage only.")
print("Clouds, NoData pixels, and valid NDVI coverage are not assessed.")
print("No new satellite data was downloaded.")
