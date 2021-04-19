from django.http import HttpResponse
from django.shortcuts import render

def data(request):
    return render(request,'main.html')
