"""
REST API urls
"""

from dashboard.api.views import AvailableProductsApiView
from django.conf.urls import url

urlpatterns = [
    url(r'', AvailableProductsApiView.as_view())
]
