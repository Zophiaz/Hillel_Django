from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<item_id>/add', views.add_item, name='add_item'),
    path('<item_id>/buy', views.buy_item, name='buy_item'),
    path('<item_id>/remove', views.remove_item, name='remove_item'),
]