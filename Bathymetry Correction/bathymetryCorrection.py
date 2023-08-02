#Changes the pixel values of a raster depending on width attribute of a centerline shapefile

#import necessary packages
import geopandas as gpd
from shapely.geometry import Point, LineString
import rasterio
import numpy as np

#Step 1: Resample the line segments of the centerline shapefile to the resolution of the raster 
# @param original_shapefile: the original centerline shapefile
# @param pixel_length: the length of each pixel in the raster
# @param output_shapefile: the output shapefile with resampled line segments
def interpolate_centerline_with_width(original_shapefile, pixel_length, output_shapefile):
    # Read the original shapefile
    gdf_original = gpd.read_file(original_shapefile)

    new_points = []

    # Iterate over each centerline segment in the original GeoDataFrame
    for row in gdf_original.iterrows():
        line = row['geometry']
        width = row['width_m']

        # Get the coordinates of the current centerline segment
        coords = line.coords

        # Add the original points with width to the list
        for j, point in enumerate(coords):
            new_point = {'ID': j, 'geometry': Point(point), 'width_m': width}
            new_points.append(new_point)

        # Interpolate points between the start and end points
        for j in range(len(coords) - 1):
            start_point = coords[j]
            end_point = coords[j + 1]

            # Calculate the distance between start and end points
            line_segment = LineString([start_point, end_point])
            distance = line_segment.length

            # Calculate the number of intervals based on pixel length
            num_intervals = int(distance / pixel_length)

            # Add the interpolated points with width to the list
            for k in range(1, num_intervals):
                fraction = k / num_intervals
                interpolated_point = line_segment.interpolate(fraction, normalized=True)
                interpolated_width = width
                new_point = {'ID': j, 'geometry': interpolated_point, 'width_m': interpolated_width}
                new_points.append(new_point)
    
    # Create a new GeoDataFrame from the list of points
    columns = ['ID', 'geometry', 'width_m']
    gdf_new = gpd.GeoDataFrame(new_points, columns=columns)

    gdf_new.crs = gdf_original.crs

    # Write the new GeoDataFrame to a shapefile
    gdf_new.to_file(output_shapefile, driver='ESRI Shapefile')


#Step 2: This function is the same as the one found in ChannelWidthDetection.py, it modifies the watermask raster 
#based on the detected widths by changing the pixel value and number of surrounding pixels. There is the option to set
# an upperbound so it does not modify channel widths greater than a user defined value
#@param tif_file: the path to the watermask raster file
#@param shapefile: the path to the centerline shapefile with widths generated from Step 1 
#@param upperbound: the upperbound for the channel width (widths above this value will not be modified)
#@param pixel_length: the length of the pixel in metres 
#@param output_file: the path to the output raster file
#@param change_value: the value subtracted from the original pixel value 
#@param pixel_bound: pixels below or above this value will not be modified

def modifyChannelWidths(tif_file, shapefile, width_bound, pixel_length, output_file, change_value, pixel_bound):
    # Read TIFF file
    with rasterio.open(tif_file) as src:
        raster_data = src.read(1)

    # Read centerline shapefile
    gdf = gpd.read_file(shapefile)
    gdf = gdf.to_crs(src.crs)

    modified_raster_data = np.copy(raster_data)

    edited = np.zeros_like(raster_data, dtype=bool)

    for line, width in zip(gdf['geometry'], gdf['detected']):
        # Check if the width exceeds the upperbound, skip this iteration
        if width == width_bound:
            continue

        # Iterate over each point on the centerline segment
        for point in line.coords:
            # Check if the point is within the raster extent
            if src.bounds.left <= point[0] <= src.bounds.right and src.bounds.bottom <= point[1] <= src.bounds.top:
                # Extract the row and column indices of the corresponding pixel
                row, col = src.index(point[0], point[1])

                # Access width value from gdf and set the width of the channel
                channel_width = int(width / pixel_length)  # Divide the width by 10m and cast as integer

                halved = int(channel_width / 2)

                if halved < 1:
                    halved = 1

                #pixel bound was example -3 
                region = modified_raster_data[row - halved: row + halved + 1, col - halved: col + halved + 1] > pixel_bound

                # Combine conditions using bitwise AND (&) to check both flag and edited matrix
                flag_new_pixels = region & ~edited[row - halved: row + halved + 1, col - halved: col + halved + 1]

                # Apply the modifications only to the pixels that are flagged as new (not edited before)
                #change value example is 3 
                modified_raster_data[row - halved: row + halved + 1, col - halved: col + halved + 1][flag_new_pixels] -= change_value

                # Update the 'edited' matrix to mark the newly modified pixels as edited
                edited[row - halved: row + halved + 1, col - halved: col + halved + 1][flag_new_pixels] = True

                print("Changed channel width at point: ({}, {})\n width is {}".format(row, col, width))

    # Copy the metadata from the source raster file
    meta = src.meta.copy()

    # Create a new raster file with the modified data
    with rasterio.open(output_file, 'w', **meta) as dst:
        dst.write(modified_raster_data, 1)
