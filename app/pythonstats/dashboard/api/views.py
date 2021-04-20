"""
REST API Views
"""
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from dashboard.models import AvailableProducts
from rest_framework.views import APIView

from .serializers import AvailableProductSerializer


class AvailableProductsApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Get all products

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        data = AvailableProducts.objects.raw('SELECT * FROM products')
        return JsonResponse(list(data), safe=False)

    def post(self, request, *args, **kwargs):
        """
        Get quantity for a specific product. Accepts the product id
        in the `product_id` field

        :param request: The request to process
        :param args:    Arguments
        :param kwargs:  Keyword arguments
        :return:    Product JSON result
        """
        product_id = request.data.get("product_id")
        data = AvailableProducts.objects.raw("Select * from products where product_id like '{}'".format(product_id))
        return JsonResponse(list(data), safe=False)
