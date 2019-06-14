import gdal
import affine
import numpy as np 
import rasterio
import utm

urls = [
			 './19971001/19971001_B1.TIF',
             './19971017/19971017_B1.TIF',
             './19971102/19971102_B1.TIF',
             './19971118/19971118_B1.TIF',
             './19981004/19981004_B1.TIF',
             './19981020/19981020_B1.TIF',
             './19981105/19981105_B1.TIF',
             './19981121/19981121_B1.TIF',
             './19981207/19981207_B1.TIF',
             './19981223/19981223_B1.TIF',
             './19991124/19991124_B1.TIF',
             './19991226/19991226_B1.TIF',
             './20081015/20081015_B1.TIF',
             './20081031/20081031_B1.TIF',
             './20081116/20081116_B1.TIF',
             './20081202/20081202_B1.TIF',
             './20081218/20081218_B1.TIF',
             './20091102/20091103_B1.TIF',
             './20091119/20091119_B1.TIF',
             './20091205/20091205_B1.TIF',
             './20101021/20101021_B1.TIF',
             './20101106/20101106_B1.TIF',
             './20101208/20101208_B1.TIF',
             './20101224/20101224_B1.TIF',
             './20111024/20111024_B1.TIF',
             './20111109/20111109_B1.TIF',
             './20171016/20171016_B1.TIF',
             './20171101/20171101_B1.TIF',
             './20171117/20171117_B1.TIF',
             './20171203/20171203_B1.TIF',
             './20171219/20171219_B1.TIF',
             './20181003/20181003_B1.TIF',
             './20181010/20181010_B1.TIF',
             './20181019/20181019_B1.TIF',
             './20181026/20181026_B1.TIF',
             './20181104/20181104_B1.TIF',
             './20181127/20181127_B1.TIF',
             './20181222/20181222_B1.TIF'
		]

def pixel2coord(col, row, a):
	"""Returns global coordinates to pixel center using base-0 raster index"""
	xp = a[1] * col + a[2] * row + a[1]* 0.5 + a[2] * 0.5 + a[0]
	yp = a[4]* col + a[5] * row + a[4]* 0.5 + a[5]* 0.5 + a[3]
	return(xp, yp)


# latitudes and longitude values of the rectangular region
lat1=29+(23/60)+(29/3600)
lng1=79+(27/60)+(58/3600)
lat2=29+(23/60)+(28/3600)
lng2=79+(27/60)+(9/3600)

lat3=29+(22/60)+(45/3600)
lng3=79+(27/60)+(9/3600)
lat4=29+(22/60)+(44/3600)
lng4=79+(27/60)+(59/3600)

[easting1,northing1,zoneNumber1,zoneLetter1] = utm.from_latlon(lat1, lng1)
[easting2,northing2,zoneNumber2,zoneLetter2] = utm.from_latlon(lat2, lng2)
[easting3,northing3,zoneNumber3,zoneLetter3] = utm.from_latlon(lat3, lng3)
[easting4,northing4,zoneNumber4,zoneLetter4] = utm.from_latlon(lat4, lng4)

e=easting1-easting2
n=northing2-northing3

imgNum = 3
bandnum = [1,2,3,4,5,6,7]
year= 1



cube=np.full((1350,1350,20,7),None)

for x in range(0,imgNum):
	
	img = gdal.Open(urls[x])
	imgGeoTransf = img.GetGeoTransform()

	row = img.RasterYSize
	col = img.RasterXSize

	bandNo = int(urls[x][-5])

	for i in range(0,row):
		for j in range(0,col):
			utm=pixel2coord(j,i,imgGeoTransf)
			utmX=int(utm[0])
			utmY=int(utm[1])
			if((utmY>easting1 and utmY<easting2) and (utmX>northing1 and utmX<northing4)):
				cube[utmX][utmY][year][bandNo]=img.GetRasterBand(1).ReadAsArray()[i][j]
				print(cube[utmX][utmY][year][bandNo],end=' ')
			else:
				print('sed',end=' ')







 