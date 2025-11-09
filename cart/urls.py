# cart/urls.py
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add/<str:name>/', views.add_to_cart, name='add_to_cart'),
    path('increment/<str:product_name>/', views.increment, name='increment'),
    path('decrement/<str:product_name>/', views.decrement, name='decrement'),
    path('remove/<str:product_name>/', views.remove_from_cart, name='remove_from_cart'),
]
