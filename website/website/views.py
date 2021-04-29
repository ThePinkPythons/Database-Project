from django.shortcuts import render

args = {"today": 55, "yesterday": 20, "last_item_sold": ' LBH6UWAEK4IK', "most_items_sold": "XLS48IBKVC7C"}


def data(request):
    return render(request, 'main.html', args)
