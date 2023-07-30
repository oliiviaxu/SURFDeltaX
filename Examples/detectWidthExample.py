# Import necessary packages
from WidthDetection.ChannelWidthDetection import detectChannelWidths

if __name__ == "__main__":
    np_array_file = 'pixelValues100test.npy'  # Replace with the path to the numpy array file
    shapefile = '/Volumes/My Passport/Olivia/Bathymetry Correction/functions/shapefiles/resampled_with_width.shp'  # Replace with the path to the shapefile with centerline points
    perp_line_length = 100  # Length of the perpendicular line in meters (use the same value used in generatePerpendicularPoints)
    num_intermediate_points = 11  # Number of intermediate points per perpendicular line (use the same value used in generatePerpendicularPoints)
    output_file = 'channelWidthsTest.shp'  # Replace with the desired output shapefile name

    # Call the detectChannelWidths function with the provided parameters
    detectChannelWidths(np_array_file, shapefile, perp_line_length, num_intermediate_points, output_file)

    print("Channel widths detected and saved to {}".format(output_file))