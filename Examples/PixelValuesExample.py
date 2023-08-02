# Import necessary packages
import sys
sys.path.append('/Volumes/My Passport/Github/SURFDeltaX')
from WidthDetection.ChannelWidthDetection import generatePixelValues

# Example usage of generatePixelValues function: step 2 of 4 in the channel width detection process
#TODO: Change the input parameters 
if __name__ == "__main__":
    watermask_file = 'SURFDeltaX/Examples/files/input/avirisWatermask.tif' 
    #perpendicular points shapefile generated from generatePerpendicularPoints
    shapefile = 'perp_points_aviris.shp' 
    num_intermediate_points = 401 #Make sure it is the same as in generatePerpendicularPoints
    file_name = 'avirisPixelValues.npy' #output filename

    # Generate the pixel values
    generatePixelValues(watermask_file, shapefile, num_intermediate_points, file_name)
    print("Pixel points generated and saved to {}".format(file_name))