#Plots an AOI given two shapefiles 

import geopandas as gpd
import matplotlib.pyplot as plt

# Read the first shapefile
shapefile1 = gpd.read_file('/Volumes/My Passport/SURF/DeltaX_data/1_Outline/WLD_extendeddomain_WSG.shp')

# Read the second shapefile
shapefile2 = gpd.read_file('/Volumes/My Passport/SURF/DeltaX_data/2_MeshDenZone/WLD_Den.shp')

bounds1 = shapefile1.bounds
bounds2 = shapefile2.bounds

# Create a new figure and axes
fig, ax = plt.subplots()

# Plot the first shapefile
shapefile1.plot(ax=ax, color='blue')

# Plot the second shapefile on top of the first one
shapefile2.plot(ax=ax, color='red')

# Customize the plot as needed (e.g., add title, legend, etc.)
plt.title('WLD Mesh Den')
plt.legend(['Shapefile 1', 'Shapefile 2'])

# Show the plot
plt.show()