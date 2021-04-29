"""
REST API urls
"""

from dashboard.api.views import AvailableProductsApiView
from dashboard.api.views import PostProductsApiView
from django.conf.urls import url


urlpatterns = [
    url(r'products', AvailableProductsApiView.as_view()),
    url(r'new-product', PostProductsApiView.as_view())
]
