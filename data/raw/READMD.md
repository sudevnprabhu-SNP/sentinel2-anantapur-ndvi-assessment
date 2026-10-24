# Raw Data

This directory is reserved for the original satellite data used in the project.

## Sentinel-2 Data

This project uses Sentinel-2B Level-2A satellite imagery acquired on **9 October 2026**.

- **Product:** `S2B_MSIL2A_20261009T050719_N0513_R019_T43PGS_20261009T090129.SAFE`
- **Tile:** T43PGS
- **Bands used:** B04 (Red), B08 (Near-Infrared), and the Scene Classification Layer (SCL)
- **Spatial resolution:** 10 m for B04 and B08

## Download the Data

The original Sentinel-2 product is not included in this GitHub repository because the complete product is large.

1. Visit the [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/).
2. Search for Sentinel-2 Level-2A imagery covering Anantapur, Andhra Pradesh, India.
3. Select the acquisition date **9 October 2026** and the corresponding T43PGS tile.
4. Download the required product and extract it locally.
5. Keep the original data in this directory when running the project locally, following the file paths specified in the project scripts.

## Repository Policy

- Original satellite imagery is excluded from Git tracking.
- Large raw data files should remain on the local computer or be shared through an appropriate external data repository.
- Processed outputs and project results are documented separately in the main project README.

**Note:** The raw satellite data must be downloaded separately before running processing steps that depend on it.
