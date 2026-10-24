
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"

print("--- SEARCHING FOR SENTINEL-2 SCL FILES ---")

scl_files = list(RAW_DIR.rglob("*SCL_20m.jp2"))

if not scl_files:
    print("No SCL_20m.jp2 file found.")
else:
    print(f"Found {len(scl_files)} SCL file(s):")
    for file in scl_files:
        print(file)
