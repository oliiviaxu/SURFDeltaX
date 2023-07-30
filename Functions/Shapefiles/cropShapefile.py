#This function crops the centerline shapefile to the extent of the raster.

import geopandas as gpd
import rasterio
from shapely.geometry import box

# Read the original shapefile
shapefile = '/Volumes/My Passport/SURF/DeltaX_data/4_Centerlines/mississippi_river_centerline_cleaned_10x2_edges_2023.04.10.shp'
gdf = gpd.read_file(shapefile)

watermask_file = '/Volumes/My Passport/Olivia/Bathymetry Correction/rasters/modified_watermask.tif'

with rasterio.open(watermask_file) as src:
    watermask_data = src.read(1)
    transform = src.transform
    bounds = src.bounds

# Create a GeoDataFrame representing the raster bounds as a polygon
raster_polygon = gpd.GeoDataFrame({'geometry': [box(bounds.left, bounds.bottom, bounds.right, bounds.top)]},
                                   crs=src.crs)

# Crop the shapefile to the bounds of the raster using intersection
cropped_gdf = gpd.overlay(gdf, raster_polygon, how='intersection')

# Write the cropped GeoDataFrame to a new shapefile
output_shapefile = 'cropped_shapefile.shp'
cropped_gdf.to_file(output_shapefile)

print("Cropped shapefile has been written to:", output_shapefile)