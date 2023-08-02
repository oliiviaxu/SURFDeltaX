# Import necessary packages
import sys
sys.path.append('/Volumes/My Passport/Github/SURFDeltaX')
from WidthDetection.ChannelWidthDetection import modifyChannelWidths

#Example usage of modifyChannelWidths function, step 4 of 4 in the channel width detection process
if __name__ == "__main__":
    #Replace with raster of region 
    tif_file = '/Volumes/My Passport/SURF/DeltaX_data/ang20210822t141334_rfl_brdf.tif'
    #Replace with output of detectChannelWidths Shapefile
    shapefile = 'channelWidthsAVIRIS.shp'
    upperbound = 2000  # Replace with your desired upperbound value
    pixel_length = 5  # Length of the pixel in meters (use the same value used in generatePerpendicularPoints and detectChannelWidths)
    output_file = 'modifiedAVIRISRaster.tif'  # Replace with the desired output raster file name
    change_value = 3
    pixel_bound = -3

    # Call the modifyChannelWidths function with the provided parameters
    modifyChannelWidths(tif_file, shapefile, upperbound, pixel_length, output_file, change_value, pixel_bound)

    print("Modified raster saved to {}".format(output_file))

