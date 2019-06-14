import gdal
import numpy as np
import affine
import os
import utm



ds = gdal.Open('first.tif')

# unravel GDAL affine transform parameters
c, a, b, f, d, e = ds.GetGeoTransform()

def pixel2coord(col, row):
    """Returns global coordinates to pixel center using base-0 raster index"""
    xp = a * col + b * row + a * 0.5 + b * 0.5 + c
    yp = d * col + e * row + d * 0.5 + e * 0.5 + f
    return(xp, yp)

print(pixel2coord(1010,1244))

img = ds.GetRasterBand(1).ReadAsArray(0,0,ds.RasterXSize,ds.RasterYSize)

print(img[1010][1244])

def getPixel(geoCoord,source):
    x,y = geoCoord[0],geoCoord[1]
    forwardT = affine.Affine.from_gdal(*source.GetGeoTransform())
    reverseT = ~forwardT
    px,py = reverseT*(x,y)
    px,py = int(px),int(py) 
    print('px is '+str(px))
    print('py is '+str(py))
    pxCoord = px,py
    dataArray = np.array(source.GetRasterBand(1).ReadAsArray())
    return dataArray[pxCoord[0]][pxCoord[1]]

geoX,geoY = pixel2coord(1010,1244)
print(getPixel([geoX,geoY],ds))


