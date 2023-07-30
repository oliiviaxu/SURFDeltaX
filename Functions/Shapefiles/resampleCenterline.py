#This function resamples the centerline shapefile by interpolating points along the line segments
#by an interval that is defined by the user. 

# Import necessary packages
import geopandas as gpd
from shapely.geometry import Point, LineString

# Resamples the centerline shapefile and outputs a new shapefile with the resampled points and width
#field
# @param original_shapefile: the original shapefile with the centerline and width field
# @param cropped_shapefile: the shapefile with the centerline that has been cropped to the extent of the
def resample_with_width(original_shapefile, cropped_shapefile, pixel_length, output_shapefile):
    # Read the original shapefile
    gdf_original = gpd.read_file(original_shapefile)

    # Read the cropped shapefile
    gdf = gpd.read_file(cropped_shapefile)
    gdf.to_crs(gdf_original.crs)

    perp_points = []  # Store the points 

    # Iterate over each centerline segment in the original GeoDataFrame
    for i, row in gdf.iterrows():
        line = row['geometry']
        # Get the width_m field, read shapefile to determine name of width field 
        width = row['width_m']

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

            # Interpolate points between the parallel lines
            for k in range(num_intervals):
                fraction = float(k) / num_intervals
                point = line.interpolate(fraction, normalized=True)
                perp_points.append({'ID': i, 'geometry': point, 'orig_width': width})
                count += 1
        print(count)

    # Create a new GeoDataFrame from the list of points
    gdf_new = gpd.GeoDataFrame(perp_points)
    gdf_new.crs = gdf_original.crs

    # Write the new GeoDataFrame to a shapefile
    gdf_new.to_file(output_shapefile, driver='ESRI Shapefile')