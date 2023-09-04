from django.urls import path
from userauths import views



urlpatterns = [
    path("handlesignup", views.handlesignup, name='handlesignup'),
    path("handlelogin", views.handlelogin, name='handlelogin'),
    path("handlelogout", views.handlelogout, name='handlelogout'),
    path("dashboard", views.dashboard, name='dashboard'),
    path('reset-password', views.reset_password, name='reset_password'),
    path('reset-password-confirm/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),
    path('profile_information', views.profile_information, name='profile_information'),
    path("otp_verify", views.otp_verify, name='otp_verify'),  # Add this line for OTP verification

    path('manage_addresses/', views.manage_addresses, name='manage_addresses'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('add_address/', views.add_address, name='add_address'),
    path('view_order/<int:order_id>/', views.view_order, name='view_order'),
    path('cancel_order_product/<int:order_id>/', views.cancel_order_product, name='cancel_order_product'),

    path('invoice/<int:order_id>/', views.invoice_view, name='invoice'),
    path('download_invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),










]
