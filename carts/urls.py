from django.urls import path
from .import views

urlpatterns = [
    path("",views.cart,name='cart'),
    path("add_cart/<int:product_id>/",views.add_cart,name='add_cart'),
    path("remove_cart/<int:product_id>/<int:cart_item_id>/",views.remove_cart,name='remove_cart'),
    path("remove_cart_item/<int:product_id>/",views.remove_cart_item,name='remove_cart_item'),
    path("remove_cart_item/<int:product_id>,<int:cart_item_id>/",views.remove_cart_item,name='remove_cart_item'),
    # path("checkout_page/<int:grand_total>/",views.checkout_page,name='checkout_page'),
    path("checkout/<int:grandtotal>/",views.checkout,name='checkout'),



    # path('razorpaycheck', views.razorpaycheck,name='razorpaycheck',),
    # path('myorders', views.myorders,name='myorders'),
    # path('myorders/<int:order_id>/', views.myorders, name='myorders'),

    # path('order_success_razorpay/<int:order_id>/', views.order_success_razorpay, name='order_success_razorpay'),


    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove_from_wishlist/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add_to_cart_from_wishlist/<int:wishlist_item_id>/', views.add_to_cart_from_wishlist, name='add_to_cart_from_wishlist'),


    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),



    path('proceed_to_pay/<int:grandtotal>/', views.proceed_to_pay, name='proceed_to_pay'),
    path('place_order/', views.place_order, name='place_order'),


 path("callback/", views.callback, name="callback"),

path('ordersuccess/', views.ordersuccess, name='ordersuccess'),

    






]
