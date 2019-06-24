import json
import numpy as np
import datacube
import requests
import xarray
import pandas as pd
import geopy.distance
from osgeo import gdal,ogr

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from myapp.models import *

from myapp.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


'''
*if the user is logged in already, then home page is rendered
*else directed to login page

'''
@login_required
def index(request):
	if request.user.is_authenticated:
		return render(request,'home.html')
	return render(request,'index.html')

def special(request):
	return HttpResponse("You are logged in !")

'''
directs to login page, authentication is nullified
'''
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/myapp/user_login/')

'''
Called for registering

*receives request from frontend when user tries to register
*request has the information to be registered
*if type of request=POST, saves the user details in the SQLITE3 database
*else registration page is rendered again
*


'''
def register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		# print(user_form)
		profile_form = UserProfileInfoForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			# our_user = UserProfileInfo(user = user_form.save(),indicesList = "'NDVI':'(nir-r)/(nir+r)'")
			# print(our_user)
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			# our_user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			# userInfo = UserProfileInfo.objects.all()
			# print(userInfo)
			if 'profile_pic' in request.FILES:
				print('found it')
				profile.profile_pic = request.FILES['profile_pic']
			profile.save()
			registered = True
		else:
			print(user_form.errors,profile_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileInfoForm()
	return render(request,'registration.html',
						  {'user_form':user_form,
						   'profile_form':profile_form,
						   'registered':registered})
'''
Called for loggin in
*request has the username and password given in by the user
This function-
*after receiving request(POST) for login, authenticates the requesting user's 
password and username
*if successful, directed to home page
*login page rendered again in case the request is not of the type POST

'''
def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		t_res={}
		t_res['username']=username
		t_res['password']=password
		# print(t_res)
		#need to return this response
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request,user)
				#return HttpResponseRedirect(reverse('index'))
				#go to the map interface after this
				return redirect('/myapp/home/')
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'login.html', {})

'''
stores the id of the user logging in and renders home page

'''	
@login_required
def home(request):
	id = request.user.id
	# print(request.user)
	user = UserProfileInfo.objects.get(user = request.user)
	# print('hi')
	print(user)

	return render(request,'home.html')

def login(request):
	return render(request,'login.html')

dc = 0
measurements = 0
products = 0

@login_required
def loadCube(request):
	global dc
	global measurements
	global products
	dc = datacube.Datacube()
	products = ['ls7_level1_usgs', 'ls5_level1_usgs']
	measurements = set(dc.index.products.get_by_name(products[0]).measurements.keys())
	for prod in products[1:]:
		measurements.intersection(dc.index.products.get_by_name(products[0]).measurements.keys())
	res = {}
	return JsonResponse(res)


'''

Called for acquiring band arrays for the clicked lat/long from the framed datacube
Request has the lat/long of the clicked point
*on receiving request from frontend after clicking on the map, loads the sent lat,long
*loads data from the datacube for the acquired lat/long combination in the form of a 3D array--*combined*
*extracts all the respective bands from this array
*stores these band arrays in a dictionary which is used as a response to the request
'''
@login_required
def getUTM(request):
	global dc
	global measurements
	global products
	res = {}
	if request.method == 'POST':
		latlng = json.loads( request.body.decode('utf-8') )
		lat = latlng['lat']
		lng = latlng['lng']
		query = {
			'time': ('1995-01-01', '2219-12-12'),
			'lat': (lat,lat),
			'lon': (lng,lng)
		}

			# find similarly named measurements

		datasets = []
		notEmptyDataset = 0
		for prod in products:
			ds = dc.load(product=prod,output_crs="EPSG:3577", resolution=(-15, 15), measurements=measurements, **query)
			if (not ds.variables):
				continue
			else:
				notEmptyDataset = 1
				# print(ds)
				ds['product'] = ('time', np.repeat(prod, ds.time.size))
				datasets.append(ds)
		if notEmptyDataset:
			combined = xarray.concat(datasets, dim='time')
			ds = combined.sortby('time')  # sort along time dim
			[red,green,blue,nir,swir1,swir2,dates] = [ds.red.values,ds.green.values,ds.blue.values,ds.nir.values,ds.swir1.values,ds.swir2.values,ds.red.time.values]
			res['message'] = 'Data recieved Successfully'
			res['error'] = 'No Error'
			res['red'] = red.tolist()
			res['blue'] = blue.tolist()
			res['green'] = green.tolist()
			res['nir'] = nir.tolist()
			res['swir1'] = swir1.tolist()
			res['swir2'] = swir2.tolist()
			res['time'] = []
			for d in dates:
					ts = pd.to_datetime(d)
					res['time'].append(ts.strftime('%Y-%m-%d'))
		else:
			res['error'] = 'Empty Dataset'
	else:
		res['error'] = 'Not recieved a post request'
	 
	#  print(res)
	return JsonResponse(res)

'''
This function acquires the indexformula for the requested indexname
*on receiving the request, first stores the indexname
*searches the index list of the current user for the above indexname
*if found, indexformula along with indexname returned as JSONresponse

'''
@login_required
def getIndexFormula(request):    	 
	 res = {}
	 
	 if request.method == 'POST':
			reqObj = json.loads( request.body.decode('utf-8') )
			tmp = reqObj['indexName'].split(':')[0]
			indexName = tmp[0:len(tmp)-1]
			print('indexNAme is '+indexName)
			usr = UserProfileInfo.objects.get(user = request.user)
			lst = usr.indicesList.split(' ')
			indexFormula = ''
			for i in lst:
				ind = i.split(':')[0]
				if(ind == indexName):
					indexFormula = i.split(':')[1]
			res['message'] = 'Data recieved Successfully'
			res['error'] = 'No Error'
			res['index'] = {
				'indexName' : indexName,
				'indexFormula' : indexFormula
			}
			
	 else:
			res['error'] = 'Not recieved a post request'
	 
	#  print(res)
	 return JsonResponse(res)

	
'''
Called for saving the customized index for the respective user
receives request(with index name and formula) for saving the index for that logged in user
*joins the indexname and indexformula with a ':'

*concatenates the above string to the index list of that user
*keeps adding the indices with a ' ' between them

'''	
@login_required
def saveIndex(request):
	 res = {}
	 
	 if request.method == 'POST':
			# print('hi')
			reqObj = json.loads( request.body.decode('utf-8') )
			indexName = reqObj['indexName']
			indexFormula = reqObj['indexFormula']
			res['message'] = 'Index saved Successfully'
			res['error'] = 'No Error'
			# print(reqObj)
			newIndex = indexName+':'+indexFormula
			usr = UserProfileInfo.objects.get(user = request.user)
			lst = usr.indicesList
			if(lst == ''):
				lst+=newIndex
			else:
				lst+=' '+newIndex
			usr.indicesList = lst
			# print(newIndex)
			usr.save()
	 else:
			res['error'] = 'Not recieved a post request'
	 print(res)
	 return JsonResponse(res)

'''
Called for getting the custom indexes and formulae of the user
If the request type is GET-
*splits the indiceslist of the respective user with ' ' as the delimiter
*further splits the obtained objects with ':' to separate out indexname and indexformula
*makes a list of all the indexnames and formulae
*returns these as dict

'''	
@login_required
def getIndices(request):
	 if request.method == 'GET':
			loggedUser = UserProfileInfo.objects.get(user = request.user)
			indicesObjects = loggedUser.indicesList.split(' ')
			print(loggedUser)
			print(indicesObjects)
			indicesNames = []
			indicesFormulas = []
			for i in indicesObjects:
				indicesNames.append(i.split(':')[0])
				indicesFormulas.append(i.split(':')[1])
			print(indicesNames)
			res = {
				'indicesNames' : indicesNames,
				'indicesFormulas' : indicesFormulas
			}
			res['message'] = 'Index saved Successfully'
			res['error'] = 'No Error'
	 else:
			res['error'] = 'Not recieved a get request'
	#  print(res)
	 return JsonResponse(res)

'''
Called for drawing the terrain profiles
Request has the array of lat/long covered by the poly-line pointers
returns an array of elevation at all the above acquired points



'''	
@login_required
def getElevations(request):
	SAMPLES = 3601 
	if request.method == 'POST':
		print('request for terrain profile')
		reqObj = json.loads( request.body.decode('utf-8') )
		latLngs = reqObj['latLngArray']
		hgt_file = 'N29E079.hgt'
		aster_file = 'ASTGTM2_N29E079\ASTGTM2_N29E079_dem.tif'
		elevArr = []
		coords1 = (latLngs[0]['lat'],latLngs[0]['lng'])
		elevationDataFound = 0
		
		latLowerBound = int(hgt_file[1:3])
		latUpperBound = latLowerBound + 1

		lngLowerBound = int(hgt_file[4:7])
		lngUpperBound = lngLowerBound + 1

		res = {}
		for i in latLngs:
			lat = i['lat']
			lon = i['lng']
			if (lat < latLowerBound or lat > latUpperBound or lon < lngLowerBound or lon > lngUpperBound):
				res['error'] = 'Empty Dataset'
				return JsonResponse(res)

		src_filename = aster_file
		src_ds=gdal.Open(src_filename) 
		gt=src_ds.GetGeoTransform()
		rb=src_ds.GetRasterBand(1)

		with open(hgt_file, 'rb') as hgt_data:
		# Each data is 16bit signed integer(i2) - big endian(>)
			elevations = np.fromfile(hgt_data, np.dtype('>i2'), SAMPLES*SAMPLES).reshape((SAMPLES, SAMPLES))
			for i in latLngs:
				lat = i['lat']
				lon = i['lng']
				lat_row = int(round((lat - int(lat)) * (SAMPLES - 1), 0))
				lon_row = int(round((lon - int(lon)) * (SAMPLES - 1), 0))
				px,py=map2pixel(lon,lat,gt)
				val = float(rb.ReadAsArray(px,py,1,1))
				ans =  elevations[SAMPLES - 1 - lat_row, lon_row].astype(int)

				coords2 = (lat,lon)
				dist = geopy.distance.vincenty(coords1,coords2).km
				elevArr.append({'elevation':{'srtm':float(ans),'aster':val},'distance':dist})
				print(ans)
				print(dist)
			res['error'] = 'no error'
			res['elevationProfile'] = elevArr

		return JsonResponse(res)

def map2pixel(mx,my,gt):
	"""
	Convert from map to pixel coordinates.
	Only works for geotransforms with no rotation.
	"""

	px = int((mx - gt[0]) / gt[1]) #x pixel
	py = int((my - gt[3]) / gt[5]) #y pixel

	return px,py
'''
returns the number of lines in a file

'''
def length(fname):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
	return i + 1
'''
Called for getting the extent of footprints
*for ech metadata file, splits the file lines with '=' to form key value pairs
*retruns an array of the acuired lat/long of the 4 corners of each file

'''
@login_required
def getFootprints(request):
	arr = []
	if request.method == 'GET':
		files = satelliteMetadataFiles.objects.all()
		for file in files:
			name = file.filename
			filePath = str(name)
			fileLength = length(filePath)
			i=0
			with open(filePath) as f:
				d = {}
				for line in f:
					i=i+1
					if(i == fileLength):
						break
					(key, val) = line.split(' = ')
					if(key == '    CORNER_UL_LON_PRODUCT' or key == '    CORNER_UL_LAT_PRODUCT' or key == '    CORNER_UR_LON_PRODUCT' or key == '    CORNER_UR_LAT_PRODUCT' or key == '    CORNER_LL_LON_PRODUCT' or key == '    CORNER_LL_LAT_PRODUCT' or key == '    CORNER_LR_LON_PRODUCT' or key == '    CORNER_LR_LAT_PRODUCT'):
						d[key] = float(val[:len(val)-1])
					if(key == '    CORNER_UL_LAT_PRODUCT'):
						print([key,float(val[:len(val)-1])])
			arr.append(d)
			# print(arr)
	return JsonResponse({'dict':arr,'error':'false'})
