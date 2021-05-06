from django.shortcuts import render
import requests
args = {"today": 55, "yesterday": 20, "last_item_sold": ' LBH6UWAEK4IK', "most_items_sold": "XLS48IBKVC7C"}

def GetDatabaseData():
    r = requests.get('http://127.0.0.1:8000/dashboard/api/from-csv')
    return r.text

def data(request):
    r = GetDatabaseData()
    print(r)
    return render(request, 'main.html', args)
