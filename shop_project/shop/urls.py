from tkinter.font import names

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'shop'  # <--- important for {% url 'shop:...' %}

urlpatterns = [
    #path('profile/',views.profile,name='profile'),
    path('', views.start, name='start'),
    path('search_list/',views.search_list,name='search_list'),
    path('category/<slug:slug>/', views.category_view, name='category_view'),
    path('product/<str:name>/',views.product_detail,name='product_detail'),
    path('products/', views.product_request, name='product_request'),
    path('order-history/', views.order_history, name='order_history'),


    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)