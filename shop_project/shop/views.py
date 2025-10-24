from itertools import product

from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.template.context_processors import request
from django.views.decorators.http import require_http_methods

from cart.views import _cart_id

from .models import Category, Product


# Create your views here.

from django.shortcuts import render, redirect

from orders.models import Order



def start(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    sort = request.GET.get('sort')

    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    return render(request,'shop/start.html',{'categories':categories,'products':products[:10],'request':request})

def search_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()
    if query:
        filtering = products.filter(name__icontains=query)
    else:
        filtering = Product.objects.none()
    context = {
        'query':query,
        'filtering':filtering
    }
    return render(request,'shop/search_list.html',context)
def category_view(request,slug):
    category = get_object_or_404(Category,slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'shop/category_products.html', {
        'category': category,
        'products': products,
        'categories': categories
    })
def product_detail(request,name):
    product = get_object_or_404(Product,name=name)
    return render(request,'shop/product_info.html',{'product':product})

def product_request(request):
    products = Product.objects.all()
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    return render(request,'shop/filter.html',{'products':products,
                                              'request':request})



def order_history(request):
    orders = Order.objects.filter(session_key=_cart_id(request))
    return render(request,'shop/order_history.html',{'orders':orders})