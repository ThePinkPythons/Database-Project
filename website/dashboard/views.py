from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render

from .models import AvailableProducts


def productsgraph(request):
    return render(request, '')


def products_by_id(request):
    """
    Returns product information

    :param request: The request to process
    :return:    A JSON response containing products and their quantities
    """
    data = AvailableProducts.objects.all()
    return JsonResponse(serializers.serialize(data), safe=False)
