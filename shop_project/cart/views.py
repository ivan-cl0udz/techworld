from itertools import product
from tkinter.font import names

from django.shortcuts import render, get_object_or_404, redirect
from urllib.parse import unquote

from .models import Cart, CartItem
from shop.models import Product

# Create your views here.
#Display the cart (cart_view)

#Add a product to the cart (add_to_cart)

#Update quantity (update_cart)

#Remove an item (remove_from_cart)

import uuid

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    if not cart:
        # Fallback if session key still not set
        cart = str(uuid.uuid4())
    return cart

def add_to_cart(request, name):
    product = get_object_or_404(Product, name=name)

    # Отримати або створити кошик
    cart, created = Cart.objects.get_or_create(cart_code=_cart_id(request))

    # Отримати або створити товар у кошику
    cart_item, item_created = CartItem.objects.get_or_create(
        products=product,
        cart=cart
    )

    # Якщо товар уже існує — збільшуємо кількість
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart')



def cart(request):
    cart, created = Cart.objects.get_or_create(cart_code=_cart_id(request))  # ✅ unpack tuple
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.products.price * item.quantity for item in cart_items)

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })




def decrement(request, product_name):
    cart = Cart.objects.get(cart_code=_cart_id(request))
    decoded_name = unquote(product_name)
    product = get_object_or_404(Product, name=decoded_name)
    cart_item = get_object_or_404(CartItem, products=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart')

def increment(request, product_name):
    cart = Cart.objects.get(cart_code=_cart_id(request))
    decoded_name = unquote(product_name)  # ✅ Розкодування пробілів
    product = get_object_or_404(Product, name=decoded_name)
    cart_item = get_object_or_404(CartItem, products=product, cart=cart)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:cart')

def remove_from_cart(request, product_name):
    cart = Cart.objects.get(cart_code=_cart_id(request))
    decoded_name = unquote(product_name)
    product = get_object_or_404(Product, name=decoded_name)
    cart_item = get_object_or_404(CartItem, products=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart')


