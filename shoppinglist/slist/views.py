from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import defaults
import django.views.defaults

from .models import ShoppingList, UserToList, MallList, Item


def index(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/user/login/')
    user_list = UserToList.objects.filter(user_id=request.user.id).first()

    #new_result = [itm.__dict__ for itm in result]
    if request.method == "POST":
        item = request.POST.get('item')
        amount = request.POST.get('amount')
        shop = request.POST.get('shop')
        shop_object = MallList.objects.filter(pk=int(shop)).first()
        item_object = Item(name=item, shop_id=shop_object)
        item_object.save()

        new_item = ShoppingList(list_id=user_list.list_id, item_id=item_object, quantity=amount)
        new_item.save()

    result = list(ShoppingList.objects.filter(list_id=user_list.list_id, status = 'available').all())

    return render(request, 'item_form.html',
                  {'shopping_list_data': result, "shops": MallList.objects.all()})


def buy_item(request, item_id):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/user/login/')
    user_list = UserToList.objects.filter(user_id=request.user.id).first()

    if request.method == "POST":
        buy_date = request.POST.get('buy_date')
        price = request.POST.get('price')
        slist_raw = ShoppingList.objects.filter(list_id=user_list.list_id, item_id_id=item_id).first()
        slist_raw.price = price
        slist_raw.buy_date = buy_date
        slist_raw.status = 'bought'
        slist_raw.save()

    result = (ShoppingList.objects.filter(list_id=user_list.list_id, status='available').all())
    return render(request, 'bought.html', {'shopping_list_data': result})


def remove_item(request):
    if not request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/user/login/')
    user_list = UserToList.objects.filter(user_id=request.user.id).first()
    result = ShoppingList.objects.filter(list_id=user_list.list_id).exclude(buy_date__isnull=False).all()
    if request.method == "POST":
        item_id = ShoppingList.item_id
        item_obj = ShoppingList.objects.filter(item_id=item_id).first()
        for raw in result:
            item_obj.delete()

    return render(request, 'remove_form.html', {'shopping_list_data': result})



