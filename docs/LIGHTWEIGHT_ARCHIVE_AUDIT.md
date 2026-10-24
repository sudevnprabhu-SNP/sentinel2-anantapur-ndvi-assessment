# Lightweight archive audit

This package was checked on 24 October 2026.

## Included
- Numbered Python scripts `01`–`35`
- Summary CSVs and exported figures
- `Three_Mandals_NDVI_Classes_20261009.tif`
- `Three_Mandals_Study_Area.geojson` and supporting boundary files
- QGIS project
- Two notebooks
- Updated README, metadata, requirements, and Results and Discussion report

## Not included / must be restored for full pipeline rerun
- Original Sentinel-2 `.SAFE` product in `data/raw/`
- `data/processed/Anantapur_NDVI_20261009.tif`
- `data/processed/Anantapur_NDVI_Masked_20261009.tif`
- `data/processed/Anantapur_NDVI_District_Clipped_20261009.tif`
- `data/processed/Three_Mandals_NDVI_Clipped_20261009.tif`

The missing TIFFs are required by upstream processing and zonal-analysis scripts. The ZIP can be used to inspect the retained results, CSVs, figures, class raster, boundary, and QGIS project, but the entire pipeline cannot be rerun until the missing rasters are restored or regenerated from the original inputs. Do not delete the user's separate original data or working project.
