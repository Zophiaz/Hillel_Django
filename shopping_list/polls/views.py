from django.shortcuts import render
from django.http import HttpResponse
from .models import ShoppingList, UserToList, MallList, Item


def index(request):
    user_list = UserToList.objects.filter(user_id=1).first()
    result = ShoppingList.objects.filter(list_id=user_list.list_id)
    new_result = [itm.__dict__ for itm in result]
    return HttpResponse(str(new_result))


def add_item(request):
    return HttpResponse("Add Item")


def buy_item(request):
    return HttpResponse("Buy Item")


def remove_item(request):
    return HttpResponse("Remove Item")
