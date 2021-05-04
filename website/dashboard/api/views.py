"""
REST API Views
"""

from dashboard.api.serializers import AvailableProductSerializer
from dashboard.models import AvailableProducts
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AvailableProductsApiView(APIView):
    """
    Available Products API View
    """
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
        product_id = request.GET.get("product_id", None)
        supplier_id = request.GET.get("supplier_id", None)
        if product_id:
            if supplier_id:
                data = AvailableProducts.objects.filter(product_id=product_id, supplier_id=supplier_id)
            else:
                data = AvailableProducts.objects.filter(product_id=product_id)
        elif supplier_id:
            data = AvailableProducts.objects.filter(supplier_id=supplier_id)
        else:
            data = AvailableProducts.objects.all()
        return HttpResponse(serializers.serialize('json', data))

    def post(self, request, *args, **kwargs):
        """
        Get quantity for a specific product. Accepts the product id
        in the `product_id` field

        :param request: The request to process
        :param args:    Arguments
        :param kwargs:  Keyword arguments
        :return:    Product JSON result
        """
        product_id = request.POST.get("product_id", None)
        supplier_id = request.POST.get("supplier_id", None)
        if product_id:
            if supplier_id:
                data = AvailableProducts.objects.filter(product_id=product_id, supplier_id=supplier_id)
            else:
                data = AvailableProducts.objects.filter(product_id=product_id)
        elif supplier_id:
            data = AvailableProducts.objects.filter(supplier_id=supplier_id)
        else:
            data = AvailableProducts.objects.all()
        return HttpResponse(serializers.serialize('json', data))


class PostProductsApiView(APIView):
    """
    Posts API Products
    """

    def get(self, request, *args, **kwargs):
        """
        Fail the request

        :param request: Request
        :param args:
        :param kwargs:
        :return: A failed response
        """
        return JsonResponse({"status": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """
        Post a new product to the database

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Mapped keyword
        :return:    JSON response related to the success of the request
        """
        data = {
            "product_id": request.data.get("product_id"),
            "quantity": int(request.data.get("quantity")),
            "wholesale_price": float(request.get("wholesale_price")),
            "sale_price": float(request.get("sale_price")),
            "supplier_id":  request.get("supplier_id")
        }
        serializer = AvailableProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
