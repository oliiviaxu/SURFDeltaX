# Import necessary packages
from WidthDetection.ChannelWidthDetection import generatePixelValues

# Example usage of generatePixelValues function
if __name__ == "__main__":
    # Define input parameters
    #replace with filepath 
    watermask_file = '/Github/Examples/files/watermask.tif' 
    #perpendicular points shapefile generated from generatePerpendicularPoints
    shapefile = 'perp_points_100.shp' 
    num_intermediate_points = 11 # Length of the pixel in meters
    file_name = 'pixelValues100test.npy' #output filename

    # Generate the pixel values
    generatePixelValues(watermask_file, shapefile, num_intermediate_points, file_name)
    print("Pixel points generated and saved to {}".format(file_name))