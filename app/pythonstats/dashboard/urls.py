"""
URLS for dashboard
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    #path('admin/', admin.site.urls),
    url(r'api/', include("dashboard.api.urls")),
]
