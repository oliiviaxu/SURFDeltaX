#Resampling the centerline for width detection is necessary for the points along the 
#centerline. This is done before running the detectWidthExample.py script. 

# Import necessary packages
import sys
sys.path.append('/Volumes/My Passport/Github/SURFDeltaX')
from Functions.Shapefiles.resampleCenterline import resample_with_width

# Example usage of resample_with_width function: step 2b of 4 in the channel width detection process
#TODO: Change the input parameters
if __name__ == "__main__":
    shapefile = 'SURFDeltaX/Examples/files/input/aviris_centerline.shp'
    #same as in generatePerpendicularPoints
    pixel_length = 5 
    #same as in generatePerpendicularPoints
    output_shapefile = 'resampled_with_width.shp'

    resample_with_width(shapefile, pixel_length, output_shapefile)