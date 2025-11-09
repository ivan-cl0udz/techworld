from itertools import product

from django.core.checks import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.template.context_processors import request
from django.views.decorators.http import require_http_methods
from .forms import UserRegisterForm,UserLoginForm

from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

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


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('shop:login')
    else:
        form = UserRegisterForm()
    return render(request,'shop/register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('shop:start')  # or your start page
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'shop/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Ви вийшли з системи.")  # ✅ info works here
    return redirect('shop:start')

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


def profile_view(request):
    return render(request, 'shop/profile.html')
def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        # Guest orders by session key
        cart_code = request.session.session_key
        if not cart_code:
            request.session.create()
            cart_code = request.session.session_key
        orders = Order.objects.filter(session_key=cart_code).order_by('-created_at')

    return render(request, 'shop/order_history.html', {'orders': orders})
