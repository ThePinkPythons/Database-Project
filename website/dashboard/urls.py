"""
URLS for dashboard
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    url('api/', include("dashboard.api.urls")),
]
