"""
REST API Views

@author Andrew Evans
"""
import uuid

from dashboard.models import AvailableProducts
from dashboard.models import Order
from django.core import serializers
from django.http import HttpResponse
from rest_framework.views import APIView


class GetOrdersView(APIView):
    """
    Obtains orders
    """

    def get_products(self, data):
        """
        Get the products from the requested parameters. Will package an error.

        :param data:    The data to process
        :return:    An appropriate HTTP Response
        """
        pass

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

    def process_data(self, data):
        """
        Process request data

        :param data:    The data to process
        :return: The request
        """
        product_id = data.get("product_id", None)
        quantity = data.get("quantity", "1")
        author_id = data.get("author", None)
        address = data.get("address", None)
        city = data.get("city", None)
        state = data.get("state", None)
        zip = data.get("zip", None)
        status = data.get("status", None)
        message = "Not All Parameters Provided. Check the Documentation"
        if product_id and quantity and author_id and address and city and state \
                and zip and status:
            # create an order id
            order_id = str(uuid.uuid4())
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
                        item_price = data[0]['price']
                        item_quantity = data[0]['quantity']
                        if item_price and item_quantity:
                            total_price = float(item_price) * float(quantity)
                            new_quantity = item_quantity - quantity

                            # update the quantity
                            data.update(quantity=new_quantity)

                            # create the order
                            order = Order(
                                order_id=order_id,
                                product_id=product_id,
                                quantity=quantity,
                                price=item_price,
                                total=total_price,
                                author_id=author_id,
                                address=address,
                                city=city,
                                state=state,
                                zip=zip,
                                status=status)
                            order.save()

                            # return order
                            return HttpResponse(serializers.serialize('json', order), 'application/json')
                        else:
                            message = "Item Price and Item Quantity Not Found in Database"
                    else:
                        message = "No Items Left to Order"
                else:
                    message = "Product ID Not Found in Database"
            else:
                message = "Order ID Already In Database"
        response = HttpResponse(serializers.serialize('json', {"Success": False, "Message": message}))
        response.status_code = 500
        return response

    def get(self, request, *args, **kwargs):
        """
        Get all products

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        data = request.GET
        return self.process_data(data)

    def post(self, request, *args, **kwargs):
        """
        Creates a product. Requires that all parameters except price be supplied.

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        data = request.POST
        return self.process_data(data)


class CancelOrdersView(APIView):
    """
    Cancels orders
    """

    def cancel_order(self, data):
        """
        Cancel an order using its order id. Does not throw an error if the order was already cancelled.

        :param data: The request data to process
        :return: The HTTP Response when complete
        """
        order_id = data.get("order_id", None)
        message = "Missing order_id Parameter"
        if order_id is not None:
            data = Order.objects.filter(order_id=order_id)
            if data.count() > 0:
                data.update(status="cancelled")
                return HttpResponse(serializers.serialize('json', {"success": True}))
            else:
                message = "Order Does Not Exist"
        return HttpResponse(serializers.serialize('json', {"success": False, "message": message}))

    def get(self, request, *args, **kwargs):
        """
        Get all products

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        data = request.GET.get("order_id", None)
        return self.cancel_order(data)


    def post(self, request, *args, **kwargs):
        """
        Get all products

        :param request: Request to process
        :param args:    Arguments
        :param kwargs:  Keyword mapped arguments
        :return:     A JSON response
        """
        data = request.POST.get("order_id", None)
        return self.cancel_order(data)


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
