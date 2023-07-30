# Description: This script reads the watermask raster data and the original shapefile, 
#and creates a numpy array of pixel values for each centerline segment. 

import geopandas as gpd
import rasterio 
import numpy as np

# Read the watermask raster data
#TODO: change the file name
watermask_file = 'genWatermask.tif' 

with rasterio.open(watermask_file) as src:
    watermask_data = src.read(1)
    transform = src.transform

# Read the original shapefile
#TODO: change the file name
shapefile = 'perp_points_aviris_5.shp' 
gdf = gpd.read_file(shapefile)
gdf = gdf.to_crs(src.crs)

num_intermediate_points = 401

# Create an empty list to store the pixel values
res = []
counter = 0
curr_row = []
default = 0

# Iterate over each centerline segment in the original GeoDataFrame
for line in gdf['geometry']:
    
    # Get the coordinates of the current centerline segment
    for point in line.coords:
        # Extract the row and column indices of the corresponding pixel
        if src.bounds.left <= point[0] <= src.bounds.right and src.bounds.bottom <= point[1] <= src.bounds.top:
            row, col = src.index(point[0], point[1])
            pixel_value = watermask_data[row, col]
        else:
            pixel_value = curr_row[-1] if counter != 0 else default 
        
        print(pixel_value)

        curr_row.append(pixel_value)
        counter += 1

        # Check if the current row has 15 elements, then append it to the result list and reset counter and curr_row
        if counter == num_intermediate_points:
            res.append(curr_row)
            counter = 0
            curr_row = []

# Create a numpy array from the list of pixel values
np_array = np.array(res)

#Save the numpy array to .npy file
# TODO: change the file name
np.save('AVpixels.npy', np_array)