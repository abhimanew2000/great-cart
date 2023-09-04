# adminauth/urls.py
from django.urls import path
from adminauth import views

urlpatterns = [
    path('admin_signin', views.admin_signin, name='admin_signin'), 
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('userinfo', views.userinfo, name='userinfo'),
    path('categorylist', views.categorylist, name='categorylist'),
    path('add_category', views.add_category, name='add_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('productlist', views.productlist, name='productlist'),
    path('add_product', views.add_product, name='add_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('add_variation/', views.add_variation, name='add_variation'),
    path('variantlist/', views.variantlist, name='variantlist'),
    path('delete_variation/<int:variation_id>/', views.delete_variation, name='delete_variation'),
    path('edit_variation/<int:variation_id>/', views.edit_variation, name='edit_variation'),

    path('orderlist/', views.orderlist, name="orderlist"),
    path('manage_orderstatus/<int:id>/', views.manage_orderstatus, name="manage_orderstatus"),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('productgallery/', views.productgallery_list, name='productgallery_list'),
    path('productgallery/add/', views.add_gallery, name='add_gallery'),
    path('productgallery/edit/<int:gallery_id>/', views.edit_gallery, name='edit_gallery'),
    path('productgallery/delete/<int:gallery_id>/', views.delete_gallery, name='delete_gallery'),



    path('sales_report/', views.sales_report, name='sales_report'),
    path('cancel_report/', views.cancel_report, name='cancel_report'),
    path('stock_report/', views.stock_report, name='stock_report'),


    path('coupons/', views.coupon_list, name='couponlist'),
    path('coupon/add/', views.add_coupon, name='add_coupon'),  # Add this line

    path('coupon/<int:pk>/', views.edit_coupon, name='edit_coupon'),  # Add this line
    path('coupon/<int:pk>/delete/', views.delete_coupon, name='delete_coupon'),









]
