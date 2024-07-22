"""
URL configuration for streeboutique project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.header_footer, name='header_footer'),
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('search/', views.search, name='search'),
    path('product/<str:id>', views.product, name='product'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name ='register'),
    path('login/', views.user_login, name ='login'),
    path('logout/', views.user_logout, name='logout'),
    path('term_condition/', views.term_condition, name='term_condition'),
    path('private_policy/', views.private_policy, name='private_policy'),
    path('faq/', views.faq, name='faq'),
    # path('order_tracking/', views.order_tracking, name='order_tracking'),
    path('about_us/', views.about_us, name='about_us'),
     path('service/', views.service, name='service'),


    #account
    path('order_page/', views.order_page, name='order_page'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),

    #login

    path('forget_pwd/', views.forget_pwd, name='forget_pwd'),
    path('varify/', views.varify, name='varify'),
    path('change_pwd/', views.change_pwd, name='change_pwd'),

    #wishlit
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    #cart
    path('cart/', views.cart_details, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart_clear/', views.cart_clear, name='cart_clear'),
    path('place_order/', views.place_order, name='place_order'), 
    path('invoice/<int:order_id>/', views.invoice, name='invoice'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
