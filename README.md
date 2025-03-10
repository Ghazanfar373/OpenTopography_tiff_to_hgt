# TIFF to HGT Converter

A Python utility to convert GeoTIFF elevation data files to SRTM HGT format, primarily for use with Mission Planner and other applications that require SRTM elevation data.

## Overview

This tool converts elevation data from GeoTIFF format to SRTM HGT format, maintaining compatibility with Mission Planner's terrain data requirements. It automatically handles coordinate system conversion and follows SRTM naming conventions.

## Features

- Converts GeoTIFF files to SRTM HGT format
- Automatically handles big-endian byte ordering
- Supports standard SRTM dimensions (1201x1201 and 3601x3601)
- Implements proper SRTM naming conventions (e.g., N00E000.hgt)
- Handles NoData values appropriately
- Provides informative console output during conversion
## Data Sources

### GeoTIFF Data Sources
- [OpenTopography Portal](https://portal.opentopography.org/datasets) - Provides access to high-resolution topography data including:
  - Global and Regional DEMs
  - High-Resolution Topography
  - USGS 3DEP Data
  - NOAA Coastal Lidar
  - Community Contributed Datasets

The OpenTopography portal offers various data formats and resolutions, making it an excellent source for GeoTIFF elevation data that can be converted using this tool. The portal includes datasets from multiple sources such as:
- Arctic DEM
- SRTM (GL1 & GL3)
- NASADEM
- Various regional and local high-resolution datasets
### Reference SRTM Data Sources
- [CGIAR-CSI SRTM](http://srtm.csi.cgiar.org/srtmdata/)
- [NGAC SRTM 90m DEM](https://www.ngac.gov/data/srtm-90m-digital-elevation-model-dem-data)
- [NASA EARTHDATA](https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/)
## Prerequisites

- Python 3.x
- Required Python packages:
  - numpy
  - GDAL (osgeo)

## Installation

1. Clone this repository:
