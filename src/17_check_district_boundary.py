
from pathlib import Path
import json

# Project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Find the GeoJSON file inside data/raw
matches = list(
    (PROJECT_DIR / "data" / "raw" / "district_nwic_geojson").rglob("district_nwic.GeoJSON")
)

if not matches:
    print("ERROR: district_nwic.GeoJSON was not found.")
    print("Check that the extracted file is inside data/raw.")
    raise SystemExit

geojson_path = matches[0]
print(f"Boundary file: {geojson_path}")

# Read district data
with geojson_path.open("r", encoding="utf-8") as file:
    data = json.load(file)

print(f"\nTotal district features: {len(data['features'])}")

# Search for Anantapur in Andhra Pradesh
print("\n--- MATCHING DISTRICTS ---")

matches_found = 0

for feature in data["features"]:
    properties = feature.get("properties", {})

    district = str(properties.get("district", "")).strip()
    state = str(properties.get("state_name", "")).strip()

    if district.lower() == "anantapur":
        matches_found += 1
        print(f"District: {district}")
        print(f"State: {state}")
        print(f"Properties: {properties}")
        print(f"Geometry type: {feature['geometry']['type']}")
        print("-" * 40)

if matches_found == 0:
    print("Anantapur was not found under that exact name.")
    print("We will inspect the available district names next.")
