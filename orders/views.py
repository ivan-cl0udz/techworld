from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ShippingAddressForm


from .models import Order, ShippingAddress

from cart.models import Cart, CartItem
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ShippingAddressForm


from .models import Order, ShippingAddress
from cart.models import Cart, CartItem

from cart.views import get_cart


def checkout_view(request):
    if request.user.is_authenticated:
        # Logged-in user: use their DB-based cart
        cart,created= Cart.objects.get_or_create(user=request.user, paid_status=False)
    else:
        # Guest: use session cart
        cart = get_cart(request)

    # --- 2️⃣ Gather items and total ---
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.products.price * item.quantity for item in cart_items)

    # --- 3️⃣ Handle form submission ---
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.save()

            # --- 4️⃣ Create order depending on user state ---
            if request.user.is_authenticated:
                order = Order.objects.create(
                    user=request.user,
                    total_price=total,
                    shipping_address=shipping_address,
                )
            else:
                if not request.session.session_key:
                    request.session.create()
                order = Order.objects.create(
                    session_key=request.session.session_key,
                    total_price=total,
                    shipping_address=shipping_address,
                )

            # Optional: copy delivery info for easier access
            order.full_name = shipping_address.full_name
            order.email = shipping_address.email
            order.phone = shipping_address.phone
            order.save()

            # --- 5️⃣ Send confirmation email ---
            send_mail(
                subject="Підтвердження замовлення",
                message=(
                    f"Вітаємо, {shipping_address.full_name}!\n\n"
                    f"Ми отримали ваше замовлення з міста {shipping_address.city}.\n"
                    f"Дякуємо, що обрали TechWorld!"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[shipping_address.email],
                fail_silently=False,
            )

            # --- 6️⃣ Mark cart as paid and clear items ---
            cart.paid_status = True
            cart.save()
            cart_items.delete()

            return redirect('orders:order_success')
    else:
        form = ShippingAddressForm()

    # --- 7️⃣ Render checkout page ---
    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total,
    })



def order_success(request):
    return render(request, 'orders/order_success.html')
