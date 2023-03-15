from django.shortcuts import render
from django.http import HttpResponse
from django.views import defaults
import django.views.defaults

from .models import ShoppingList, UserToList, MallList, Item


def index(request):
    user_list = UserToList.objects.filter(user_id=1).first()

    #new_result = [itm.__dict__ for itm in result]
    if request.method == "POST":
        item = request.POST.get('item')
        amount = request.POST.get('amount')
        shop = request.POST.get('shop')
        shop_object = MallList.objects.filter(pk=int(shop)).first()
        item_object = Item(name=item, shop_id=shop_object)
        new_item = ShoppingList(list_id=user_list.list_id, item_id=item_object, quantity=amount)


    result = list(ShoppingList.objects.filter(list_id=user_list.list_id).exclude(buy_date__isnull=False).all())

    return render(request, 'item_form.html',
                  {'shopping_list_data': result, "shops": MallList.objects.all()})
#.filter(list_id=user_list.list_id)


def add_item(request):
    user_list = UserToList.objects.filter(user_id=1).first()

    if request.method == "POST":
        item = request.POST.get('item')
        amount = request.POST.get('amount')
        shop = request.POST.get('shop')
        shop_object = MallList.objects.filter(pk=int(shop)).first()
        item_object = Item(name=item, shop_id=shop_object)
        item_object.save()

        new_item = ShoppingList(list_id=user_list.list_id, item_id=item_object, quantity=amount)
        new_item.save()

    #result = list(ShoppingList.objects.filter(list_id=user_list.list_id).all())

    return render(request, 'add_form.html', {"shops": MallList.objects.all()})


def buy_item(request):
    user_list = UserToList.objects.filter(user_id=1).first()

    #for raw in db_raw:
    if request.method == "POST":
        db_raw = ShoppingList.objects.filter(list_id=user_list.list_id).exclude(buy_date__isnull=False).first()
        buy_date = request.POST.get("buy_date")
        price = request.POST.get("price")
        new_raw = ShoppingList(list_id=user_list.list_id, item_id=db_raw.item_id, quantity=db_raw.quantity,
                               buy_date=buy_date, price=price)
        new_raw.save()
        db_raw.delete()

    result = (ShoppingList.objects.filter(list_id=user_list.list_id).exclude(buy_date__isnull=False).all())
    return render(request, 'buy_form.html', {'shopping_list_data': result})


def remove_item(request):
    user_list = UserToList.objects.filter(user_id=1).first()
    result = ShoppingList.objects.filter(list_id=user_list.list_id).exclude(buy_date__isnull=False).all()
    if request.method == "POST":
        item_id = ShoppingList.item_id
        item_obj = ShoppingList.objects.filter(item_id=item_id)
        for raw in result:
            item_obj.delete()

    return render(request, 'remove_form.html', {'shopping_list_data': result})
