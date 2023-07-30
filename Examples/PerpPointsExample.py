from WidthDetection.ChannelWidthDetection import generatePerpendicularPoints

# Example usage of generatePerpendicularPoints function
if __name__ == "__main__":
    # Define input parameters
    #Replace with filepath to centerline shapefile
    shapefile = '/Volumes/My Passport/SURF/DeltaX_data/Shape/WLD_centerline_Extend.shp'
    pixel_length = 5  # Length of the pixel in meters
    perp_line_length = 2000  # Length of the perpendicular line in meters
    num_intermediate_points = 401  # Number of intermediate points to interpolate between start and end points
    output_file_name = 'perp_points_aviris.shp'  # Replace with the desired output shapefile name

    # Call the generatePerpendicularPoints function with the provided parameters
    generatePerpendicularPoints(shapefile, pixel_length, perp_line_length, num_intermediate_points, output_file_name)

    print("Perpendicular points generated and saved to {}.shp".format(output_file_name))
