# Results and Discussion
## Sentinel-2 NDVI Assessment of Three Mandals in Anantapur

**Scene date:** 9 October 2026  
**Study areas:** Anantapur Urban, Anantapur Rural, and Bukkaraya Samudram  
**Sensor/product:** Sentinel-2B MSI Level-2A  
**Spatial resolution:** 10 m for B04 and B08  
**CRS:** EPSG:32643

## Abstract

This project assessed the spatial distribution of the Normalized Difference Vegetation Index (NDVI) over Anantapur Urban, Anantapur Rural, and Bukkaraya Samudram using a Sentinel-2B Level-2A scene acquired on 9 October 2026. Red (B04) and near-infrared (B08) reflectance were used to calculate NDVI. An SCL-based cloud/shadow masking workflow was applied, and the raster was clipped to the combined study boundary. Descriptive NDVI classes and mandal-level summary statistics were calculated. The mean NDVI across valid pixels was 0.2786, and valid-data coverage within the study boundary was 93.07%. The 0.15 to below 0.30 class was the largest class, accounting for 47.59% of valid area. Bukkaraya Samudram had the highest mean NDVI (0.2913), while Anantapur Urban had the lowest (0.2252). Because this is a single-date assessment and NDVI is not a unique land-cover identifier, conclusions are limited to observed index patterns on the acquisition date.

## 1. Introduction

Satellite remote sensing provides spatially consistent observations for examining vegetation-related spectral variation across administrative areas. NDVI combines red and near-infrared reflectance to express their normalized difference. Green vegetation often absorbs red light and reflects near-infrared energy, but NDVI values are also affected by soil background, moisture, vegetation stage, built surfaces, atmosphere, shadows, and mixed pixels.

The objective was to calculate NDVI from Sentinel-2 imagery, describe its distribution across three mandals, estimate the area represented by five NDVI intervals, and compare summary statistics among the mandals.

## 2. Data and study area

The analysis used a Sentinel-2B MSI Level-2A scene acquired on 9 October 2026, tile T43PGS. Bands B04 (red) and B08 (near-infrared) have 10 m native pixel size. The working coordinate reference system was WGS 84 / UTM zone 43N (EPSG:32643).

The study area comprises Anantapur Urban, Anantapur Rural, and Bukkaraya Samudram mandals. Their boundaries were combined into a three-feature study-area GeoJSON and used to extract the relevant raster pixels.

## 3. Methodology

### 3.1 NDVI calculation

NDVI was calculated as:

\[
NDVI = \frac{B08 - B04}{B08 + B04}
\]

where B08 represents near-infrared reflectance and B04 represents red reflectance. Pixels with invalid inputs, NoData values, non-finite results, or a zero denominator must be excluded from summary calculations.

### 3.2 Cloud and invalid-data masking

A mask based on the Sentinel-2 Scene Classification Layer (SCL) was used in the processing workflow to remove selected cloud/shadow and other unsuitable classes. The reported invalid-data fraction can include masked pixels and other NoData. It should not be interpreted as cloud percentage without a separate cloud-only calculation.

### 3.3 Clipping and zonal statistics

The masked NDVI raster was clipped to the combined three-mandal boundary. A pixel-centre geometry mask was used for study-area coverage calculations. For each mandal, valid-pixel counts, valid-data coverage, mean, median, standard deviation, minimum, and maximum NDVI were summarized.

### 3.4 NDVI classes and area

Valid NDVI pixels were grouped into five descriptive classes. The raster pixel size is 10 m × 10 m, corresponding to 100 m² per pixel in the projected CRS. Class area was calculated from valid pixel counts.

| Class | NDVI range | Share of valid area |
|---|---|---:|
| 1 | Below 0.00 | 1.16% |
| 2 | 0.00 to < 0.15 | 12.81% |
| 3 | 0.15 to < 0.30 | 47.59% |
| 4 | 0.30 to < 0.45 | 27.51% |
| 5 | 0.45 and above | 10.93% |

These intervals are descriptive index classes and are not validated land-cover labels.

## 4. Results

### 4.1 Overall statistics

| Metric | Result |
|---|---:|
| Valid-data coverage within the study boundary | 93.07% |
| Valid NDVI area | 505.889 km² |
| Mean NDVI | 0.2786 |
| Median NDVI | 0.2634 |
| Standard deviation | 0.1259 |
| Minimum NDVI | −0.2507 |
| Maximum NDVI | 0.6997 |

The most common class was 0.15 to below 0.30, covering 240.761 km² (47.59% of valid area). Classes with NDVI at or above 0.30 covered 194.442 km² (38.44%). Classes below 0.15, including negative values, covered 70.686 km² (13.97%).

### 4.2 Comparison between mandals

| Mandal | Valid area (km²) | Valid coverage | Mean NDVI | Median NDVI | Standard deviation |
|---|---:|---:|---:|---:|---:|
| Anantapur Urban | 51.508 | 92.40% | 0.2252 | 0.2122 | 0.1344 |
| Anantapur Rural | 225.552 | 92.44% | 0.2779 | 0.2631 | 0.1173 |
| Bukkaraya Samudram | 228.830 | 93.85% | 0.2913 | 0.2737 | 0.1288 |

Bukkaraya Samudram had the highest mean NDVI and the largest Class 5 share (13.41%). Anantapur Urban had the lowest mean NDVI and the largest combined share of Classes 1 and 2 (30.90%). Anantapur Rural had 51.05% of its valid area in Class 3, while Bukkaraya Samudram had 45.35% in Class 3.

### 4.3 Interpretation

The results show that the three mandals had different NDVI distributions on the selected date. The relatively lower mean NDVI in Anantapur Urban is consistent with a more heterogeneous landscape that may include built-up surfaces, bare soil, and vegetation, but these causes were not independently tested in this project. The higher mean NDVI in Bukkaraya Samudram indicates higher average NDVI values in the valid pixels for this scene; it does not prove greater agricultural productivity or better crop health.

**Figure files generated by the project:**
- `figure_1_mean_ndvi_by_mandal.png` — mean NDVI comparison.
- `figure_2_ndvi_class_distribution.png` — overall NDVI class percentages.
- `figure_3_ndvi_classes_by_mandal.png` — stacked class percentages by mandal.
- `three_mandals_ndvi_map.png` — NDVI map for the three-mandal study area.
- `three_mandals_ndvi_classification.png` — five-class NDVI map.

## 5. Limitations

1. The analysis represents one acquisition date and cannot establish seasonal or long-term trends.
2. NDVI values are not unique to specific land-cover types and do not independently establish crop type, crop health, yield, or productivity.
3. Cloud/shadow masking can remove valid pixels or leave residual contamination; invalid-data coverage is not the same as cloud cover.
4. The selected class thresholds are descriptive and would need independent validation for a land-cover classification objective.
5. The findings depend on the boundary version, raster alignment, mask definitions, and input processing.

## 6. Conclusion

A Sentinel-2B Level-2A scene from 9 October 2026 was used to assess NDVI across Anantapur Urban, Anantapur Rural, and Bukkaraya Samudram. The mean NDVI across valid pixels was 0.2786, with 93.07% valid-data coverage inside the study boundary. The 0.15 to below 0.30 class dominated the valid area at 47.59%. Bukkaraya Samudram had the highest mean NDVI (0.2913), and Anantapur Urban the lowest (0.2252). These findings provide a reproducible single-date baseline for future comparisons. A multi-date analysis, independent land-cover data, and a dedicated cloud-quality assessment would be needed to investigate change or explain the observed differences.

## Reproducibility status

The submitted lightweight ZIP contains the analysis scripts, summary CSVs, figures, study boundary, classified NDVI raster, and QGIS project. The original `.SAFE` data and several intermediate NDVI TIFFs are not included. Consequently, the report's results can be inspected from the retained outputs, but the complete pipeline cannot be rerun from this ZIP alone until the missing input rasters are restored or regenerated.
