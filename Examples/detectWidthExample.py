# Import necessary packages
import sys
sys.path.append('/Volumes/My Passport/Github/SURFDeltaX')
from WidthDetection.ChannelWidthDetection import detectChannelWidths

# Example usage of detectChannelWidths function: step 3 of 4 in the channel width detection process
#TODO: Change the input parameters 
if __name__ == "__main__":
    np_array_file = 'avirisPixelValues.npy'  # Replace with the path to the numpy array file
    shapefile = 'resampled_with_width.shp'  # Replace with the path to the shapefile with centerline points
    perp_line_length = 2000  # Length of the perpendicular line in meters (use the same value used in generatePerpendicularPoints)
    num_intermediate_points = 401  # Number of intermediate points per perpendicular line (use the same value used in generatePerpendicularPoints)
    output_file = 'channelWidthsAVIRIS.shp'  # Replace with the desired output shapefile name

    # Call the detectChannelWidths function with the provided parameters
    detectChannelWidths(np_array_file, shapefile, perp_line_length, num_intermediate_points, output_file)

    print("Channel widths detected and saved to {}".format(output_file))