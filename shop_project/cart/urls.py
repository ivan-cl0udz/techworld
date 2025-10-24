from django.urls import path
from . import views

app_name = 'cart'  # <--- Add this line

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add_cart/<str:name>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increment/<str:product_name>/', views.increment, name='increment'),
    path('cart/decrement/<str:product_name>/', views.decrement, name='decrement'),
    path('cart/remove/<str:product_name>/', views.remove_from_cart, name='remove_from_cart'),
]
