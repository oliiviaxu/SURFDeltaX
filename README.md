# SURFDeltaX
SURFDeltaX is an open-source repository of pre-processing tools for the study of secondary channel networks in wetlands. This toolkit is comprised of two core functionalities: Automatic Channel Width Detection from remote sensing data and Bathymetry Data Correction. 

Numerical models of land-building processes require a custom mesh describing the topography and hydrodynamics of wetland environments, and this codebase provides a framework for enhancing the accuracy of the input data (shapefiles) needed for computational mesh generation. 

## Installation
To use the SURFDeltaX toolkit, you need to have Python installed on your system. If you don't have Python, you can download and install it from the official Python website (https://www.python.org/downloads/).

Once you have Python installed, you can install the required packages using pip, the Python package manager. Open a terminal or command prompt and run the following commands:

pip install geopandas
pip install shapely
pip install numpy
pip install rasterio
pip install matplotlib

Next, download the SURFDeltaX repository from the GitHub page. You can do this by clicking on the "Code" button and selecting "Download ZIP". Once the ZIP file is downloaded, extract its contents to a folder on your computer.Please ensure that you have the required shapefiles and raster files in the correct format (WSG 84 CRS) as mentioned in the Usage Guide section of the README. You can now use the provided scripts and functions on your shapefiles and raster files.

## Usage Guide
To get started, ensure you have a Python code editor installed on your system, and use the scripts and the functions within on shapefiles and rasters. Ensure that you have the following files for shapefiles and rasters in WSG 84 CRS: .shp (Shapefile geometry), .dbf (Shapefile attributes), .prj (Coordinate system information), .shx (Shapefile index), .cpg (Character encoding file), and .tif (Raster data). This program relies on the following Python packages: geopandas, shapely.geometry, numpy, rasterio, matplotlib, and ensure that you have them installed on your system.

### Automatic Channel Width Detection
Automatic channel Width Detection is divided into these main functions: 
1. generatePerpendicularPoints
2. generatePixelValues
3. detectChannelWidths and resampleCenterline 
4. modifyChannelWidths*
The fourth function is optional as it modifies a raster based after detecting the channel widths. The functions are called in succession, in which the output of one function is used as input to the next. 

#### generatePerpendicularPoints
This function generates points perpendicular to the centerline segments of a shapefile to form orthogonal cross sections. The function calculates the distance between the start and end points of the centerline segment. Based on user-defined parameters, it determines the number of intermediate points to be interpolated along the line segment. Next, two parallel lines are constructed at a specified distance from the original centerline, forming the cross section. By interpolating points between these parallel lines, the function ensures that the resulting points are distributed evenly and accurately represent the orthogonal cross section.

##### Parameters
- `original_shapefile` (str): Original centerline shapefile 

- `pixel_length`(float): Length of pixel in meters (resolution)

- `perp_line_length` (float): Desired length of perpendicular line segments in metres 

- `num_intermediate_points` (int): Number of intermediate points to interpolate between the parallel offsetted lines 

- `output_file_name`(str) Desire name of the output shapefile

##### Output 
This function produces a shapefile of shapely point geometries representing the orthogonal cross sections. The output shapefile is in the format of a standard shapefile, comprising multiple files: `.shp` (Shapefile geometry), `.dbf` (Shapefile attributes), `.prj` (Coordinate system information), `.shx` (Shapefile index), and `.cpg` (Character encoding file).

#### generatePixelValues
This function overlays the shapefile generated from generatePerpendicularPoints, reads the watermask raster, and outputs a numpy array with the corresponding pixel values. 

##### Parameters
- `watermask_file` (str): The path to the watermask raster file. Must be in 0-1 binary format. There is a script in this repository that can generate 0-1 binary rasters given a raster and is explained in the additional functions section.  
- `shapefile` (str): The path to the shapefile with perpendicular points (generated from generatePerpendicularPoints).
- `num_intermediate_points` (int): The number of intermediate points to interpolate between the start and end points. *Must be the same value inputted for generatePerpendicularPoints

##### Output 
The output is a numpy array containing the pixel values from the watermask raster corresponding to each point of the perpendicular cross sections. The array is saved to a .npy file, which can be used as input for subsequent data processing steps in the workflow. 

#### detectChannelWidths 
To detect channel width, first, you need to resample the centerline shapefile. You can do this by using the [resampleCenterline](#resamplecenterline) function.
This function reads the numpy array generated from the previous function, which contains information about the resampled centerline points and the orthogonal cross sections. The function then calculates the width of the channel at each centerline point based on the perpendicular lines.

##### Parameters
- `np_array_file` (str): The path to the numpy array file generated from the previous function, containing information about the resampled centerline points and cross sections.
- `shapefile` (str): The path to the shapefile containing only the centerline points (resampled) that corresponds to the numpy array.
- `perp_line_length` (float): The length of the perpendicular line in meters.
num_intermediate_points (int): The number of intermediate points per perpendicular line, which was used in generating the numpy array.
- `output_file` (str): The desired name and path for the output shapefile containing the detected channel widths.

##### Output
This function produces a new shapefile containing the detected channel widths at each centerline point. The output shapefile contains shapely point geometries representing the centerline points and an attribute column containing the detected channel widths. The output shapefile is in the format of a standard shapefile, comprising multiple files: .shp (Shapefile geometry), .dbf (Shapefile attributes), .prj (Coordinate system information), .shx (Shapefile index), and .cpg (Character encoding file).

#### modifyChannelWidths
This optional function allows users to modify a watermask raster based on the detected channel widths. It is designed to change the pixel values of the watermask raster to match the detected channel widths up to a user-defined upper bound. The function provides a way to ensure that channel widths greater than a specific value remain unmodified.

##### Parameters
- `tif_file` (str): The path to the watermask raster file to be modified.
- `shapefile` (str): The path to the shapefile containing the detected channel widths for reference.
- `width_bound` (float): The user-defined upper bound for the channel width. Widths above this value will not be modified in the raster.
- `pixel_length` (float): The length of the pixel in meters (e.g., resolution).
output_file (str): The desired name and path for the output raster file after modification.
- `change_value` (float): The value to change the pixels to, based on the detected widths.
- `pixel_bound` (float): The user-defined value to set the upper bound for pixel modification. Pixels with values greater than this bound will be modified.

##### Output
This optional function produces a new raster (.tif) file that has been modified based on the detected channel widths. The modified raster reflects the changes in channel widths with pixel values adjusted accordingly. The output raster file is in the same format as the original watermask raster, and the user-defined upper bound ensures that channel widths above the specified value are not modified.

#### Example: AVIRIS data 
This example automatically detects and exports secondary channels widths based on a single raster and shapefile. These are the expected file names and outputs when you run the example scripts. 

##### Input Files
| File Name                | Description                                               |
| -----------------------  | --------------------------------------------------------- |
| aviris_centerline.*[^1]  | Shapefile containing the original AVIRIS centerline.      |
| avirisWatermask.tif      | AVIRIS Watermask raster (0-1binary)                       |

##### Output Files
| Script                   | Output file name         | Type              |
| ------------------------ | ------------------------ | ----------------- |
| PerpPointsExample.py     | perp_points_aviris       | .shp*             |
| PixelValuesExample.py    | avirisPixelValues        | .npy              |  
| modCenterlineExample.py  | resampled_with_width     | .shp*             |         
| detectWidthExample.py    | channelWidthsAVIRIS      | .shp*             |
| modifyRasterExample.py   | modifiedAVIRISRaster     | .tif              |  
[^1]: The asterisk (*) represents all components of the shapefile.

### Bathymetry Correction 
Correcting bathymetry data consists of two main steps to improve the accuracy of  representing channel depth in raster files through the modification of pixel values and the number of pixels. 

#### Step 1: Resample Centerline with Width
The interpolate_centerline_with_width function is designed to resample the line segments of the original centerline shapefile to match the resolution of the target raster. It linearly interpolates points along each centerline segment and assigns corresponding width attributes based on the width information provided in the original centerline shapefile. The output is a new shapefile with resampled line segments and associated width attributes.

##### Parameters
- `original_shapefile` (str): The path to the original centerline shapefile.
- `pixel_length` (float): The length of each pixel in the target raster, in meters.
- `output_shapefile` (str): The path to the output shapefile that will contain the resampled line segments and width attributes.

#### Step 2: Modify Raster Based on Detected Widths
The modifyChannelWidths function is the same as that in ChannelWidthDetection.py, modifying the pixel values of a raster based on the width attribute of the centerline shapefile. It reads the raster data and changes the pixel values of the water area based on the detected widths from the centerline shapefile.

### Additional Functions
#### Rasters

##### genWatermask.py
Generates a water mask from a Sentinel-2 image. The water mask is created by setting all "no data" values in the input .tif file to 0 and all other values to 1, effectively creating a binary mask where water pixels are represented by 1 and non-water pixels by 0.

###### Parameters: 
- `input_tif` (str): The path to the input .tif file, which is the Sentinel-2 image.
- `output_tif` (str): The path to the output .tif file that will store the generated water mask.
###### Output:
The function creates a new .tif file containing the water mask, with water pixels represented as 1 and non-water pixels as 0. The output file will have the same geospatial metadata as the input image.

An example output water mask file (genWatermask.tif) is included in the example folder for reference.Please ensure that the input TIFF file contains a valid "no data" value to accurately create the water mask. 

#### Shapefiles 

#### resampleCenterline.py
<a name="resamplecenterline"></a>
Channel width detection first requires resampling the centerline shapefile without the perpendicular points. This function resamples the centerline shapefile based on the pixel length and outputs a new shapefile with the resampled points and width. 

##### Parameters
- `original_shapefile` (str): The path to the original shapefile containing the centerline and width field (optional).
- `pixel_length` (int): The desired interval length for the interpolation in meters.
- `output_shapefile` (str): The desired name and path for the output shapefile containing the resampled points.

##### Output 
This function produces a new shapefile with resampled points along the centerline segments. The output shapefile contains shapely point geometries, and the width field (if available) from the original shapefile can also be included in the resampled shapefile. The output shapefile is in the format of a standard shapefile, comprising multiple files: .shp (Shapefile geometry), .dbf (Shapefile attributes), .prj (Coordinate system information), .shx (Shapefile index), and .cpg (Character encoding file).

##### cropShapefile.py
Reads shapefile and raster, cropping shapefile based on bounds of a watermask  

##### loadShapefile.py
Loads shapefile, useful for reading bounds, head, geometry, crs 

### Contact 
If you have any questions about the algorithm, please don't hesitate to contact oxu@caltech.edu