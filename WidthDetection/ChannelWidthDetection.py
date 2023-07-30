# Olivia Xu 2023 07/28/2021
#This program detects the width of secondary channels given a centerline shapefile 
#and a watermask raster. It then outputs a shapefile with the detected widths. 

# Import necessary packages
import geopandas as gpd
from shapely.geometry import Point, LineString
import numpy as np
import rasterio
import matplotlib.pyplot as plt

#WORKING 
#Overview: To detect the width fo the secondary channels it is necessary to find the
#orthogonal line to the centerline. 
# @param original_shapefile: the original shapefile that contains the centerline
# @param shapefile: the shapefile that contains the perpendicular points
# @param pixel_length: the length of the pixel in meters
# @param perp_line_length: the length of the perpendicular line in meters
# @param num_intermediate_points: the number of intermediate points to interpolate between the start and end points
# @param output_file_name: the name of the output shapefile
# @return: None 
def generatePerpendicularPoints(shapefile, pixel_length, perp_line_length, num_intermediate_points, file_name):
    # Read the shapefile with geopandas
    gdf = gpd.read_file(shapefile)

    gdf.to_crs(gdf.crs)

    perp_points = []  # Store the perpendicular points

    # Iterate over each centerline segment in the original GeoDataFrame
    for i, row in gdf.iterrows():
        #read the field name if it is not 'geometry'
        line = row['geometry']

        if line is None:
            continue

        # Get the coordinates of the current centerline segment
        coords = line.coords

        # Interpolate points between the start and end points
        for j in range(len(coords) - 1):
            start_point = Point(coords[j])
            end_point = Point(coords[j + 1])

            # Calculate the distance between start and end points
            line_segment = LineString([start_point, end_point])
            distance = line_segment.length

            # Use a fixed number of intervals for interpolating points along the line segment
            num_intervals = int(distance / pixel_length)

            # Create two parallel lines at a distance / 2 from the original line
            parallel_line1 = line.parallel_offset(perp_line_length / 2, 'left')
            parallel_line2 = line.parallel_offset(perp_line_length / 2, 'right')

            # Interpolate points between the parallel lines
            for k in range(num_intervals):
                fraction = float(k) / num_intervals
                point_on_parallel1 = parallel_line1.interpolate(fraction, normalized=True)
                point_on_parallel2 = parallel_line2.interpolate(fraction, normalized=True)

                # Generate intermediate points along the intermediate line
                intermediate_points = np.linspace(0, 1, num_intermediate_points, endpoint=True)
                for frac in intermediate_points:
                    point = Point(
                        point_on_parallel1.x + frac * (point_on_parallel2.x - point_on_parallel1.x),
                        point_on_parallel1.y + frac * (point_on_parallel2.y - point_on_parallel1.y),
                    )
                    perp_points.append({'ID': i, 'geometry': point})

    # Create a new GeoDataFrame from the list of points
    columns = ['ID', 'geometry']
    gdf_new = gpd.GeoDataFrame(perp_points, columns=columns)
    gdf_new.crs = gdf.crs

    # Write the new GeoDataFrame to a shapefile
    gdf_new.to_file(file_name, driver='ESRI Shapefile')

#Overview: this function overlays the shapefile generated from generatePerpendicularPoints, reads the watermask 
# raster and outputs a numpy array with the corresponding pixel values
# @param watermask_file: the path to the watermask raster file
# @param shapefile: the path to the shapefile with perpendicular points
# @param num_intermediate_points: the number of intermediate points to interpolate between the start and end points

def generatePixelValues(watermask_file, shapefile, num_intermediate_points, file_name):
    # Read the watermask raster data
    with rasterio.open(watermask_file) as src:
        watermask_data = src.read(1)

    # Read the original shapefile
    gdf = gpd.read_file(shapefile)
    gdf = gdf.to_crs(src.crs)

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

            curr_row.append(pixel_value)
            counter += 1

            # Check if the current row has num_intermediate_points elements,
            # then append it to the result list and reset counter and curr_row
            if counter == num_intermediate_points:
                res.append(curr_row)
                counter = 0
                curr_row = []

    # Create a numpy array from the list of pixel values
    np_array = np.array(res)

    # Save the numpy array to .npy file
    np.save(file_name, np_array)

#this program reads the np array generated from the previous function and 
#calculates the width of the channel at each centerline point 
# @param np_array_file: the path to the numpy array file generated from previous function
# @param shapefile: the path to the shapefile with only centerline points (resampled)
# @param perp_line_length: the length of the perpendicular line
# @param num_intermediate_points: the number of intermediate points per perpendicular line

def detectChannelWidths(np_array_file, shapefile, perp_line_length, num_intermediate_points, output_file):
    # Load the numpy array from .npy file
    np_array = np.load(np_array_file)

    # Pad the numpy array with an extra column of zeros
    np_array = np.pad(np_array, ((0, 0), (0, 1)), 'constant', constant_values=0)

    flat = np_array.flatten()

    ker1 = [1, -1]

    grad1 = np.convolve(flat, ker1, mode='same')

    # Reshape the gradient with num_intermediate_points + 1 columns
    reshaped = grad1.reshape(-1, num_intermediate_points + 1)

    # Calculate the centerline index (points / 2)
    centerline_index = num_intermediate_points // 2

    # Divide the reshaped gradient into two parts (left and right)
    left_side = reshaped[:, :centerline_index + 1]
    right_side = reshaped[:, centerline_index:]  # Skip the centerline pixel

    left_side = np.flip(left_side, axis=1)

    # Find the width for each row on the left side (from the centerline towards the left)
    left_widths = np.argmax(left_side > 0, axis=1)

    # Find the width for each row on the right side (from the centerline towards the right)
    right_widths = np.argmax(right_side < 0, axis=1)

    # Combine the left and right widths
    widths = left_widths + right_widths

    # Calculate the conversion factor to convert widths to real-world units
    conversion_factor = perp_line_length / (num_intermediate_points - 1)

    # Convert the widths to real-world units
    widths = widths * conversion_factor

    # Read the original shapefile
    gdf = gpd.read_file(shapefile)

    output = []

    for i, row in gdf.iterrows():
        line = row['geometry']
        width = row['orig_width']
        # Add each point to the dataframe
        temp = {'ID': i, 'geometry': line, 'orig_width': width, 'detected': widths[i]}
        print(temp)
        output.append(temp)

    # Create a new GeoDataFrame from the list of points
    gdf_new = gpd.GeoDataFrame(output)
    gdf_new.crs = gdf.crs

    # Write the new GeoDataFrame to a shapefile
    gdf_new.to_file(output_file, driver='ESRI Shapefile')

#OPTIONAL: This function modifies the watermask raster based on the detected widths by changing the
#pixel value. It also sets an upperbound so it does not modify channel widths greater than a user 
#defined value
#@param tif_file: the path to the watermask raster file
#@param shapefile: the path to the shapefile with detected widths
#@param upperbound: the upperbound for the channel width (widths above this value will not be modified)
#@param pixel_length: the length of the pixel in metres 

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