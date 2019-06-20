from django.conf.urls import include, url
from . import views
import myapp
app_name='myapp'
urlpatterns = [
     url(r'^home/',myapp.views.home, name = 'home'),
     url(r'^getUTM/',myapp.views.getUTM, name = 'getUTM'),
     url(r'^getIndexFormula/',myapp.views.getIndexFormula, name = 'getIndexFormula'),
     url(r'^saveIndex/',myapp.views.saveIndex, name = 'saveIndex'),
     url(r'^getIndices/',myapp.views.getIndices, name = 'getIndices'),
     url(r'^register/$',views.register,name='register'),
     url(r'^user_login/$',views.user_login,name='user_login'),
     url(r'^getElevations/',myapp.views.getElevations, name = 'getElevations'),
     url(r'^loadCube/$',myapp.views.loadCube,name='loadCube'),
     url(r'^getFootprints/$',myapp.views.getFootprints,name='getFootprints'),
]