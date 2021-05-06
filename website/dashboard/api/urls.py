"""
REST API urls
"""

from dashboard.api.views import AvailableProductsApiView
from dashboard.api.views import CancelOrdersView
from dashboard.api.views import CreateOrdersView
from dashboard.api.views import PostProductsApiView
from dashboard.api.views import GetOrdersView
from dashboard.api.views import ReadCSVDataFromFile
from django.conf.urls import url


urlpatterns = [
    url(r'products', AvailableProductsApiView.as_view()),
    url(r'new-product', PostProductsApiView.as_view()),
    url(r'get-orders', GetOrdersView.as_view()),
    url(r'cancel-order', CancelOrdersView.as_view()),
    url(r'create-order', CreateOrdersView.as_view()),
    url(r'from-csv',ReadCSVDataFromFile.as_view())
]
