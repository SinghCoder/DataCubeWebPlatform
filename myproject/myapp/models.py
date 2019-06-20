from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class indices(models.Model):
	indexName = models.CharField(max_length = 10)
	indexFormula = models.CharField(max_length = 100)

	def __str__(self):
		return self.indexName

class UserProfileInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	portfolio_site = models.URLField(blank=True)
	profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
	indicesList = models.CharField(max_length = 20000,default = "NDVI:((nir-r)/(nir+r))")
	def __str__(self):
  		return self.user.username

class satelliteMetadataFiles(models.Model):
	filename = models.CharField(max_length = 100,default="")