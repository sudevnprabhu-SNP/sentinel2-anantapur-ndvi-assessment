
from pathlib import Path
import geopandas as gpd

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR / "data" / "raw"
    / "district_nwic_geojson" / "district_nwic.GeoJSON"
)

OUTPUT_FILE = (
    PROJECT_DIR / "data" / "processed"
    / "Anantapur_District_Boundary.geojson"
)

print("Loading district boundaries...")

districts = gpd.read_file(INPUT_FILE)

anantapur = districts[
    (districts["district"].str.strip().str.casefold() == "anantapur")
    & (districts["state_name"].str.strip().str.casefold() == "andhra pradesh")
].copy()

if anantapur.empty:
    raise ValueError("Anantapur district was not found.")

# Convert to WGS 84 for browser compatibility.
anantapur = anantapur.to_crs("EPSG:4326")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
anantapur.to_file(OUTPUT_FILE, driver="GeoJSON")

print("District:", anantapur.iloc[0]["district"])
print("State:", anantapur.iloc[0]["state_name"])
print("CRS:", anantapur.crs)
print("Saved:", OUTPUT_FILE)
print("File exists:", OUTPUT_FILE.exists())
