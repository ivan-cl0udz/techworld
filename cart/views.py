from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction, IntegrityError
from urllib.parse import unquote
from .models import Cart, CartItem
from shop.models import Product
import uuid


from django.db import transaction, IntegrityError

def get_cart(request):
    """
    Always returns an active (unpaid) cart for current user or session.
    Creates one if it doesn’t exist.
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, paid_status=False).first()
        if not cart:
            try:
                with transaction.atomic():
                    cart = Cart.objects.create(user=request.user, paid_status=False)
            except IntegrityError:
                cart = Cart.objects.filter(user=request.user, paid_status=False).first()
        return cart

    # Anonymous user
    if not request.session.session_key:
        request.session.create()
    cart_code = request.session.session_key

    cart = Cart.objects.filter(cart_code=cart_code, paid_status=False).first()
    if not cart:
        try:
            with transaction.atomic():
                cart = Cart.objects.create(cart_code=cart_code, paid_status=False)
        except IntegrityError:
            cart = Cart.objects.filter(cart_code=cart_code, paid_status=False).first()
    return cart

# ✅ Display the cart
def cart(request):
    cart = get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.products.price * item.quantity for item in cart_items)

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


# ✅ Add to cart
from django.http import JsonResponse

def add_to_cart(request, name):
    decoded_name = unquote(name)
    product = get_object_or_404(Product, name=decoded_name)
    cart = get_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        products=product,
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # ✅ If AJAX, send back a small JSON response (no redirect)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        total_items = CartItem.objects.filter(cart=cart).count()
        return JsonResponse({
            'message': 'Товар додано до кошика!',
            'total_items': total_items
        })

    # ✅ Otherwise normal browser redirect (fallback)
    return redirect('cart:cart')



# ✅ Increment
def increment(request, product_name):
    decoded_name = unquote(product_name)
    cart = get_cart(request)
    product = get_object_or_404(Product, name=decoded_name)
    cart_item = get_object_or_404(CartItem, cart=cart, products=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:cart')


# ✅ Decrement
def decrement(request, product_name):
    decoded_name = unquote(product_name)
    cart = get_cart(request)
    product = get_object_or_404(Product, name=decoded_name)
    cart_item = get_object_or_404(CartItem, cart=cart, products=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart')


# ✅ Remove
def remove_from_cart(request, product_name):
    decoded_name = unquote(product_name)
    cart = get_cart(request)
    product = get_object_or_404(Product, name=decoded_name)
    cart_item = get_object_or_404(CartItem, cart=cart, products=product)
    cart_item.delete()
    return redirect('cart:cart')
