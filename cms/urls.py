
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def cms (request):
    return HttpResponse('Hello, Django!') 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cms/', cms),
    path('', include('cmsApp.urls')),
]
 