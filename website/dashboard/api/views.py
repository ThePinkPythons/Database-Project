"""
REST API Views
"""

from dashboard.models import AvailableProducts
from dashboard.models import Order
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.views import APIView


class GetOrdersView(APIView):
    """
    Obtains orders
    """

    def get(self, request, *args, **kwargs):
        """
        Get all products

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        pass

    def post(self, request, *args, **kwargs):
        """
        Get all products

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        pass


class CreateOrdersView(APIView):
    """
    Creates orders
    """

    def get(self, request, *args, **kwargs):
        """
        Get all products

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        order_id = request.GET.get("order_id", None)
        data = Order.objects.filter(order_id=order_id)
        if data.count() > 0:
            data.update(status="cancelled")

    def post(self, request, *args, **kwargs):
        """
        Get all products

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        order_id = request.POST.get("order_id", None)
        data = Order.objects.filter(order_id=order_id)
        if data.count() > 0:
            data.update(status="cancelled")


class CancelOrdersView(APIView):
    """
    Cancels orders
    """

    def get(self, request, *args, **kwargs):
        """
        Get all products

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        order_id = request.GET.get("order_id", None)
        data = Order.objects.filter(order_id=order_id)
        if data.count() > 0:
            data.update(status="cancelled")

    def post(self, request, *args, **kwargs):
        """
        Get all products

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        order_id = request.POST.get("order_id", None)
        data = Order.objects.filter(order_id=order_id)
        if data.count() > 0:
            data.update(status="cancelled")


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
        return HttpResponse(serializers.serialize('json', data), 'application/json')

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
        return HttpResponse(serializers.serialize('json', data), 'application/json')


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
        product_id = request.POST.get("product_id", None)
        quantity = request.POST.get("quantity", None)
        wholesale_price = request.POST.get("wholesale_price", None)
        sale_price = request.POST.get("sale_price", None)
        supplier_id = request.POST.get("supplier_id", None)
        data = AvailableProducts.objects.filter(product_id=product_id)
        if data.count() > 0:
            data.update(
                quantity=quantity,
                wholesale_price=wholesale_price,
                sale_price=sale_price,
                supplier_id=supplier_id)
        else:
            object = AvailableProducts(
                product_id=product_id,
                quantity=quantity,
                wholesale_price=wholesale_price,
                sale_price=sale_price,
                supplier_id=supplier_id)
            object.save()
        return HttpResponse({"Success": True}, 'application/json')
