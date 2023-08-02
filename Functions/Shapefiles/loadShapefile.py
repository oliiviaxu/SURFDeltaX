import geopandas as gpd
import rasterio
import matplotlib.pyplot as plt

#TODO: add path to shapefile and watermask
shapefile = 'path/to/your/shapefile.shp'
gdf = gpd.read_file(shapefile)

#Bounds 
print(gdf.total_bounds)

print(len(gdf))

#Crs:
print(gdf.crs)

#Columns(fields)
print(gdf.head())

#Plot the shapefile
gdf.plot(ax=plt.gca(), color='red', markersize=5)
plt.show()