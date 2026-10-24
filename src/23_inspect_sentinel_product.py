
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"

print("--- SENTINEL-2 PRODUCT INVENTORY ---")

products = list(RAW_DIR.rglob("*.SAFE"))

if not products:
    print("No .SAFE product folders found.")
    print("Check the extracted Sentinel-2 data folder.")
else:
    for product in products:
        print("\nProduct folder:")
        print(product.name)

        print("Metadata files:")
        metadata_files = [
            product / "MTD_MSIL2A.xml",
            product / "manifest.safe",
        ]

        for metadata_file in metadata_files:
            if metadata_file.exists():
                print(" -", metadata_file.relative_to(PROJECT_DIR))

        granules_dir = product / "GRANULE"

        if granules_dir.exists():
            print("Granules:")
            for granule in granules_dir.iterdir():
                if granule.is_dir():
                    print(" -", granule.name)

print("\nInventory completed.")
