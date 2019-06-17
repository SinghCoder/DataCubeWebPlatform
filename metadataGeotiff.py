import rasterio
import os
import gdal
ds = gdal.Open('first.tif')
geoTransform = ds.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * ds.RasterXSize
miny = maxy + geoTransform[5] * ds.RasterYSize
print(minx,maxx,miny,maxy)