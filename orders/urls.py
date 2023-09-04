from django.urls import path
from . import views  # Update the import statement here

urlpatterns = [
    # path('place_order/', views.place_order, name='place_order'), 
    path('order_success/<int:id>/', views.order_success, name='order_success'),

    # Handle Razorpay callback
   
   
]
