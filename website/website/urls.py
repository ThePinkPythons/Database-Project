from django.conf.urls import url
from django.urls import path, include

from . import views

urlpatterns = [
	url('website/', views.data),
	url(r'dashboard/', include("dashboard.urls"))
]
