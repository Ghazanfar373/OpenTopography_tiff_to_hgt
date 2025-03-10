import os
import numpy
from osgeo import gdal
import struct

# SRTM Sources
# http://srtm.csi.cgiar.org/srtmdata/
# https://www.ngac.gov/data/srtm-90m-digital-elevation-model-dem-data
# https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/



def convert_tiff_to_hgt(input_tiff, output_hgt, nodata_value=-32768):
    """
    Convert a GeoTIFF file to SRTM HGT format for use in Mission Planner.
    
    Args:
        input_tiff (str): Path to input GeoTIFF file
        output_hgt (str): Path to output HGT file
        nodata_value (int): Value to use for no data points
    """
    # Open the raster dataset
    ds = gdal.Open(input_tiff)
    if ds is None:
        print(f"Failed to open {input_tiff}")
        return False
    
    # Get dataset properties
    band = ds.GetRasterBand(1)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    
    # Check if dimensions are compatible with SRTM format
    # SRTM files are typically 1201x1201 (1 arc-second) or 3601x3601 (3 arc-seconds)
    valid_sizes = [1201, 3601]
    if cols not in valid_sizes or rows not in valid_sizes:
        #print(f"Warning: Non-standard SRTM dimensions: {cols}x{rows}")
        #print("Standard SRTM dimensions are 1201x1201 (1 arc-second) or 3601x3601 (3 arc-seconds)")
        #print("Mission Planner might not read this file correctly")
        print("Please make sure dimensions matrix.")
    
    # Read the data
    data = band.ReadAsArray(0, 0, cols, rows).astype(numpy.int16)  # Explicitly convert to int16 when reading
    
    # Replace any NaN or no data values
    nodata_mask = (data == band.GetNoDataValue()) | numpy.isnan(data)
    data[nodata_mask] = nodata_value
    
    # HGT files store elevation as 16-bit signed integers in big-endian format
    # No need to convert data type again since we did it during reading
    
    # Write the data to binary file in big-endian format
    with open(output_hgt, 'wb') as f:
        for i in range(rows):
            # SRTM data has origin at upper-left, rows going south
            # Convert to signed 16-bit big-endian values
            row_data = data[i, :].byteswap().tobytes()  # First byteswap for big-endian, then convert to bytes
            f.write(row_data)
    
    # Get the geotransform to extract coordinates for the filename
    geotransform = ds.GetGeoTransform()
    minx = geotransform[0]
    maxy = geotransform[3]  # upper-left y
    
    # Calculate approximate lat/lon for the upper-left corner
    # This is used for naming the file according to SRTM conventions
    longitude = int(minx)
    latitude = int(maxy)
    
    # SRTM filename convention: N00E000.hgt (latitude then longitude)
    ns = 'N' if latitude >= 0 else 'S'
    ew = 'E' if longitude >= 0 else 'W'
    
    # Format with leading zeros
    lat_str = f"{abs(latitude):02d}"
    lon_str = f"{abs(longitude):03d}"
    
    srtm_filename = f"{ns}{lat_str}{ew}{lon_str}.hgt"
    
    print(f"HGT data written to: {output_hgt}")
    print(f"Suggested SRTM filename: {srtm_filename}")
    
    # Optionally rename the file to follow SRTM naming conventions
    srtm_path = os.path.join(os.path.dirname(output_hgt), srtm_filename)
    if output_hgt != srtm_path:
        print(f"Renaming to standard SRTM format: {srtm_path}")
        try:
            os.rename(output_hgt, srtm_path)
            return srtm_path
        except:
            print("Couldn't rename file. You should manually rename it to follow SRTM conventions.")
    
    return output_hgt

# Example usage
if __name__ == "__main__":
    import sys
    #print("Usage: python tiff_to_hgt.py input.tiff output.hgt")
    if len(sys.argv) < 2:
        print("Usage: python tiff_to_hgt.py input.tiff output.hgt")
        sys.exit(1)
        
    input_tiff = sys.argv[1]
    output_hgt = sys.argv[2]
    
    convert_tiff_to_hgt(input_tiff, output_hgt)