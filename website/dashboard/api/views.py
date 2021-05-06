"""
REST API Views
"""

from dashboard.models import AvailableProducts
from dashboard.models import Order
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.views import APIView
#Change to use json from django
import json

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

class ReadCSVDataFromFile(APIView):
    data  = {
    0:{"date":"","cust_email":"bia@gmail.com","product_id":"6CSX2YDY0IQM", "product_quantity":4},
    1:{"date":"","cust_email":"bia@gmail.com","product_id":"D1ILW1BNLNN7", "product_quantity":4},
    2:{"date":"","cust_email":"bia@gmail.com","product_id":"UUFK84M22NOL", "product_quantity":9}
    }

    def sort():
        """
        Function used to read nested dict data. Then convert it into one dict
        Containing the product_id and product_quantity
        """
        list = []
        output = {}
        for i in range (len(ReadCSVDataFromFile.data)):
            for j in range(ReadCSVDataFromFile.data[i]['product_quantity']):
                list.append(ReadCSVDataFromFile.data[i]['product_id'])
        while(True):
            if(len(list) == 0):
                break
            count = list.count(list[0])
            output[list[0]] = count
            for i in range (count):
                list.pop(0)
        return output

    def get(self,request):
        """
        Get all products from CSV
        :param request: Request to process
        :param args:    Arguments
        return: JSON response
        """
        return HttpResponse(json.dumps(ReadCSVDataFromFile.sort()))

class CreateOrdersView(APIView):
    """
    Creates orders
    """

    def process_data(self, data):
        """
        Process request data

        :param data:    The data to process
        :return: The request
        """
        order_id = data.get("order_id", None)
        product_id = data.get("product_id", None)
        quantity = data.get("quantity", "1")
        author_id = data.get("author", None)
        address = data.get("address", None)
        city = data.get("city", None)
        state = data.get("state", None)
        zip = data.get("zip", None)
        status = data.get("status", None)
        message = "Not All Parameters Provided. Check the Documentation"
        if order_id and product_id and quantity and author_id and address and city and state \
                and zip and status:
            # check if the order exists
            data = Order.objects.filter(order_id=order_id)
            if data.count() == 0:
                # get the product
                data = AvailableProducts.objects.filter(product_id=product_id)
                data_list = list(data)
                if len(data_list) > 0:
                    # check the quantity
                    if data[0]['quantity'] > 0:
                        # get the price
                        price = data[0]['price']
                        total_price = price * float(quantity)

                        # update the quantity

                        # create the order
                return HttpResponse()
        return HttpResponse({"Success": False, "Message": message})

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
        Creates a product. Requires that all parameters except price be supplied.

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        # get required parameters
        return


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
