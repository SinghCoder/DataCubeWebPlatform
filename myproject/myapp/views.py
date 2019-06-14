import json
import numpy as np
import datacube
import requests
import xarray
import pandas as pd

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from myapp.models import indices,UserProfileInfo

from myapp.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
	return render(request,'index.html')

def special(request):
	return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/myapp/user_login/')


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

@login_required
def getUTM(request):
	 res = {}
	 if request.method == 'POST':
			latlng = json.loads( request.body.decode('utf-8') )
			lat = latlng['lat']
			lng = latlng['lng']
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

			datasets = []
			for prod in products:
				ds = dc.load(product=prod,output_crs="EPSG:3577", resolution=(-15, 15), measurements=measurements, **query)
				ds['product'] = ('time', np.repeat(prod, ds.time.size))
				datasets.append(ds)

			combined = xarray.concat(datasets, dim='time')
			ds = combined.sortby('time')  # sort along time dim


			# print(ds.isnull())
			# print(ds.dims)
			[red,green,blue,nir,swir1,swir2,dates] = [ds.red.values,ds.green.values,ds.blue.values,ds.nir.values,ds.swir1.values,ds.swir2.values,ds.red.time.values]
			# print([red,green,blue,nir])

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
			res['error'] = 'Not recieved a post request'
	 
	#  print(res)
	 return JsonResponse(res)

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

@login_required
def getElevations(request):
	if request.method == 'POST':
		print('request for terrain profile')
		reqObj = json.loads( request.body.decode('utf-8') )
		latLngs = reqObj['latLngArray']
		queryParams = ''
		for i in latLngs:
			queryParams+=','
			queryParams+=str(i['lat'])
			queryParams+=','
			queryParams+=str(i['lng'])
		queryParams = queryParams[1:]
		print(queryParams)
		query = ('http://open.mapquestapi.com/elevation/v1/profile?key=xxJeGzM0qOcSKmEVmjPI0N09bPpiASzD&shapeFormat=raw&latLngCollection='+str(queryParams))
		print(query)
		r = requests.get(query)
		print('-----------------------------------------------------------------------------')
		elevationAPIOutput = json.loads(r.content)
		print(elevationAPIOutput)
		print('-----------------------------------------------------------------------------')
		res = {}
		if(elevationAPIOutput['info']['statuscode'] == 0):
			res['elevationProfile'] = elevationAPIOutput['elevationProfile']
			res['error'] = 'no error'
			print(res)
			return JsonResponse(res)
		else:	
			res['error'] = 'error in processing'
			return JsonResponse(res)

