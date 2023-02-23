from django.contrib import admin

from .models import ShoppingList, UserToList, MallList, Item
admin.site.register(ShoppingList)
admin.site.register(UserToList)
admin.site.register(MallList)
admin.site.register(Item)
