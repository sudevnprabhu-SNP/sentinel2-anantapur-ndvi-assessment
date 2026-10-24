# Processed Data Directory

This folder contains derived outputs, not the original Sentinel-2 `.SAFE` product.

## Which outputs are necessary?

| Output | Purpose | GitHub recommendation |
|---|---|---|
| `Anantapur_NDVI_20261009.tif` | Initial NDVI raster | Keep locally if oversized; regenerate from B04/B08 |
| `Anantapur_NDVI_Masked_20261009.tif` | NDVI after SCL cloud/shadow masking | Keep locally if oversized; regenerate from NDVI + SCL |
| `Anantapur_NDVI_District_Clipped_20261009.tif` | Intermediate district clip | Optional if final analysis uses only three mandals |
| `Anantapur_SCL_CloudMask_20261009.tif` | Derived cloud/shadow mask | Usually regenerable from SCL and processing code |
| `Anantapur_District_Boundary.geojson` | District boundary | Optional; keep only if scripts/QGIS project use it |
| `Anantapur_Urban_Rural_Bukkarayasamudram.geojson` | Combined three-mandal boundary | Keep if this is the boundary used by final workflow |
| `Three_Mandals_Study_Area.geojson` | Final study-area geometry | Keep; small input needed to reproduce the final clip |
| `Three_Mandals_NDVI_Clipped_20261009.tif` | Final clipped NDVI | Useful, but don't commit if over GitHub's normal 100 MiB limit |
| `Three_Mandals_NDVI_Classes_20261009.tif` | Exploratory classified NDVI | Useful output, but can be regenerated; don't commit if oversized |
| CSV statistics and PNG figures | Results and plots | Keep in GitHub; these are compact and show the outcome |

## Recommendation for the three very large rasters

The three files visible in the project folder—`Anantapur_NDVI_20261009.tif`, `Anantapur_NDVI_Masked_20261009.tif`, and `Anantapur_NDVI_District_Clipped_20261009.tif`—do **not** need to be uploaded to GitHub. Keep them on your computer if the scripts or QGIS project still reference them. The district-clipped intermediate is optional if your final workflow clips directly to the three-mandal study area. Before deleting local copies, search your scripts and QGIS project for their filenames.

## Data lineage

1. Download Sentinel-2B Level-2A imagery separately from the Copernicus Data Space Ecosystem.
2. Use B04 (red) and B08 (near-infrared) to calculate NDVI.
3. Apply an SCL-based cloud/shadow mask.
4. Use the three-mandal boundary: Anantapur Urban, Anantapur Rural, and Bukkaraya Samudram.
5. Generate clipped NDVI, exploratory NDVI classes, CSV summaries, maps, and figures.

## Scientific cautions

- The scene is from 9 October 2026; one date cannot establish seasonal or long-term change.
- NDVI bins are exploratory intervals, not validated land-cover classes.
- Valid-data coverage is not identical to cloud-free coverage; NoData may have multiple causes.
- Do not delete intermediate files until you verify no script or QGIS layer depends on them.
