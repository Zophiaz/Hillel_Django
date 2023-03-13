from django.shortcuts import render
from django.http import HttpResponse
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
        item_object.save()

        new_item = ShoppingList(list_id=user_list.list_id, item_id=item_object, quantity=amount)
        new_item.save()

    result = list(ShoppingList.objects.filter(list_id=user_list.list_id).all())

    return render(request, 'item_form.html',
                  {'shopping_list_data': result, "shops": MallList.objects.all()})
#.filter(list_id=user_list.list_id)


def add_item(item_id):

    return render(item_id, "add_form.html")


def buy_item(request, id, item_id):
    user_list = UserToList.objects.filter(user_id=1).first()
    bought_item = index(request.POST.get('item'))
    bought_amount = index(request.POST.get('amount'))
    bought_shop = index(request.POST.get('shop'))
    shop_obj = MallList.objects.filter(pk=int(bought_shop)).first()
    item_obj = Item(name=bought_item, shop_id=shop_obj)
    db_raw = ShoppingList.objects.filter(list_id=user_list.list_id, item_id=item_obj, quantity=bought_amount).\
        exclude(buy_date__isnull=False).first()
    if db_raw:
        if request.method == "POST":
            item = ShoppingList.objects.get(id=id)
            item.delete()
            buy_date = request.POST.get("buy_date")
            price = request.POST.get("price")
            bought_item = ShoppingList(list_id=user_list.list_id, item_id=item_obj, quantity=bought_amount,
                                       price=price, buy_date=buy_date)
            bought_item.save()

    result = (ShoppingList.objects.filter(list_id=user_list.list_id).exclude(buy_date__isnull=True).all())
    return render(request, 'buy_form.html', {'shopping_list_data': result})



def remove_item(request, id):
    user_list = UserToList.objects.filter(user_id=1).first()
    item = buy_item(index(request.POST.get('item')))
    amount = buy_item(index(request.POST.get('amount')))
    shop = buy_item(index(request.POST.get('shop')))
    shop_obj = MallList.objects.filter(pk=int(shop)).first()
    item_obj = Item(name=item, shop_id=shop_obj)
    db_raw = ShoppingList.objects.filter(list_id=user_list.list_id, item_id=item_obj, quantity=amount).\
        exclude(buy_date__isnull=False).first()
    if db_raw:
        if request.method == "POST":
            item = ShoppingList.objects.get(id=id)
            item.delete()

    return render(request, 'remove_form.html')
