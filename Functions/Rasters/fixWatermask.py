import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
import numpy as np

#Modifies watermask along centerline, accounting for narrow secondary channels not
#represented in the watermask 
def modify_raster_along_polyline(tif_file, shapefile, output_file):
    # Read TIFF file
    with rasterio.open(tif_file) as src:
        raster_data = src.read(1)

    # Read centerline shapefile
    gdf = gpd.read_file(shapefile)
    gdf = gdf.to_crs(src.crs)

    modified_raster_data = np.copy(raster_data)

    for line in gdf['geometry']:
        # Iterate over each point on the centerline segment
        for point in line.coords:
            # Check if the point is within the raster extent
            if src.bounds.left <= point[0] <= src.bounds.right and src.bounds.bottom <= point[1] <= src.bounds.top:
                # Extract the row and column indices of the corresponding pixel
                row, col = src.index(point[0], point[1])

                # Get the pixel value from the raster data
                pixel_value = modified_raster_data[row, col]

                # Print or analyze the pixel value
                if pixel_value == 0:
                    modified_raster_data[row, col] = 1
                    print("changed")

    # Copy the metadata from the source raster file
    meta = src.meta.copy()

    # Create a new raster file with the modified data
    with rasterio.open(output_file, 'w', **meta) as dst:
        dst.write(modified_raster_data, 1)