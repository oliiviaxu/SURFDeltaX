# Import necessary packages
from WidthDetection.ChannelWidthDetection import modifyChannelWidths

#Example usage of modifyChannelWidths function
if __name__ == "__main__":
    #Replace with raster of region 
    tif_file = '/Volumes/My Passport/SURF/DeltaX_data/3_Bathymetry/DeltaX_DEM_MRD_LA_2181/data/DeltaX_MultiSource_DEM_Atchafalaya_Terrebonne_Basin_2021_V1.tif'
    #Replace with output of detectChannelWidths Shapefile
    shapefile = '/Examples/files/channelWidthsTest.shp'
    upperbound = 100.0  # Replace with your desired upperbound value
    pixel_length = 10  # Length of the pixel in meters (use the same value used in generatePerpendicularPoints and detectChannelWidths)
    output_file = 'modifiedRaster.tif'  # Replace with the desired output raster file name

    # Call the modifyChannelWidths function with the provided parameters
    modifyChannelWidths(tif_file, shapefile, upperbound, pixel_length, output_file)

    print("Modified raster saved to {}".format(output_file))

