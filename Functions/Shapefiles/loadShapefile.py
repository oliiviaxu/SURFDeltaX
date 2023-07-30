import geopandas as gpd
import rasterio
import matplotlib.pyplot as plt

# Read the original shapefiles
shapefile = 'segments_cropped.shp'
gdf = gpd.read_file(shapefile)

#Bounds 
print(gdf.total_bounds)

#Plot the shapefile
gdf.plot(ax=plt.gca(), color='red', markersize=5)
plt.show()
