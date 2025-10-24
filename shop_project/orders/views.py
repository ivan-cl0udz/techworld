from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ShippingAddressForm
from cart.views import _cart_id

from .models import Order, ShippingAddress

from cart.models import Cart, CartItem
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ShippingAddressForm
from cart.views import _cart_id

from .models import Order, ShippingAddress
from cart.models import Cart, CartItem


def checkout_view(request):
    cart_code = _cart_id(request)
    cart = get_object_or_404(Cart, cart_code=cart_code)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.products.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.save()

            order = Order.objects.create(
                session_key=cart_code,
                total_price=total,
                shipping_address=shipping_address,
                full_name=shipping_address.full_name,
                email=shipping_address.email,
                phone=shipping_address.phone,
                address_line1=shipping_address.address_line1,
                address_line2=shipping_address.address_line2,
                city=shipping_address.city,
                state=shipping_address.state,
                postal_code=shipping_address.postal_code,
                country=shipping_address.country
            )

            # ✅ Send email AFTER order is created
            send_mail(
                "Order confirmation",
                f"Вітаю, {shipping_address.full_name}! Ми отримали ваше замовлення з міста {shipping_address.city}.",
                        settings.EMAIL_HOST_USER,
                [shipping_address.email],
                fail_silently=False,
            )

            cart.paid_status = True
            cart.save()
            cart_items.delete()

            return redirect('orders:order_success')
    else:
        form = ShippingAddressForm()

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total
    })



def order_success(request):
    return render(request, 'orders/order_success.html')
