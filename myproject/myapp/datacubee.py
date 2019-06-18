import json
import numpy as np
import datacube
import requests
import xarray
import pandas as pd
import geopy.distance
from osgeo import gdal,ogr
import datacube

dc = datacube.Datacube()
query = {
		'time': ('1995-01-01', '2219-12-12'),
		'lat': (lat,lat),
		'lon': (lng,lng)
		}
products = ['ls7_level1_usgs', 'ls5_level1_usgs']
# find similarly named measurements
measurements = set(dc.index.products.get_by_name(products[0]).measurements.keys())
for prod in products[1:]:
	measurements.intersection(dc.index.products.get_by_name(products[0]).measurements.keys())