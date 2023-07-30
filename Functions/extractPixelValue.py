import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
import numpy as np
from shapely.coords import CoordinateSequence

#This program extracts the pixel value and assigns it to the shapefile 
tif_file = '/Volumes/My Passport/SURF/DeltaX_data/ang20210822t141334_rfl_brdf.tif'
shapefile = 'perp_points_aviris_5.shp'

# Read TIFF file
with rasterio.open(tif_file) as src:
    raster_data = src.read(1)

# Read centerline shapefile
gdf = gpd.read_file(shapefile)
gdf = gdf.to_crs(src.crs)

# Create a list to store pixel values along with the corresponding geometries and IDs
pixel_values = []

# Iterate over each row (point) in the GeoDataFrame
for i, row in gdf.iterrows():
    point = row['geometry']

    # Check if the point is within the raster extent
    if src.bounds.left <= point.x <= src.bounds.right and src.bounds.bottom <= point.y <= src.bounds.top:
        # Extract the row and column indices of the corresponding pixel
        row, col = src.index(point.x, point.y)

        # Get the pixel value from the raster data
        pixel_value = raster_data[row, col]

        # Create a dictionary with 'ID', 'geometry', and 'pixel_value' information
        pixel_info = {'ID': i, 'geometry': point, 'pixel_value': pixel_value}
        print(pixel_info)
        # Append the pixel_info dictionary to the pixel_values list
        pixel_values.append(pixel_info)

columns = ['ID', 'geometry', 'pixel_value']
# Create a new GeoDataFrame from the list of pixel_values
new_gdf = gpd.GeoDataFrame(pixel_values, columns=columns)

# Set the CRS of the new GeoDataFrame to match the original GeoDataFrame's CRS
new_gdf.crs = gdf.crs

# Write the new GeoDataFrame to a shapefile
output_shapefile = 'aviris_with_pixel_values_3.shp'
new_gdf.to_file(output_shapefile, driver='ESRI Shapefile')