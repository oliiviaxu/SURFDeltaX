#This generates a water mask from a Sentinel-2 image. It takes the input tif file and sets all no data 
#values to 0 and everything else to 1. An example output is included in this folder. 

import rasterio
from rasterio.enums import Resampling
import numpy as np

def set_nodata_to_zero(input_tif, output_tif):
    with rasterio.open(input_tif) as src:
        # Read the raster data as a NumPy array
        data = src.read(1)

        # Get the no data value from the raster
        nodata_value = src.nodata

        # Set no data values to 0 and everything else to 1
        output_data = np.where(data == nodata_value, 0, 1)

        # Copy the metadata from the source raster
        kwargs = src.meta.copy()

        # Update the data type to be uint8 (0 or 1 values)
        kwargs.update(dtype=rasterio.float32)

        # Write the new tif file with the updated data
        with rasterio.open(output_tif, 'w', **kwargs) as dst:
            dst.write(output_data, 1)

# Input and output tif file paths
input_tif_file = '/Volumes/My Passport/SURF/DeltaX_data/ang20210822t141334_rfl_brdf.tif'
output_tif_file = 'genWatermask.tif'  # Replace with the desired output path

# Call the function to create the new tif file
set_nodata_to_zero(input_tif_file, output_tif_file)
