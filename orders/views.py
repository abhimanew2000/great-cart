from django.shortcuts import render,redirect
from carts.models import CartItem
from.models import Order,OrderProduct
import datetime
from django.contrib import messages
from userauths.models import Address
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse

# Create your views here.

def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    context = {
        'orders': orders
    }
    return render(request, 'userauth/dashboard.html', context)
def order_success(request,id):
    order = get_object_or_404(Order,id=id,user=request.user)
    order_products = OrderProduct.objects.filter(order=order)
    print(f"Order ID: {order.id}")
    print(f"Order Total: {order.order_total}")
    print(f"Number of Order Products: {order_products.count()}")
    print(f"Order Products: {order_products}")
    context = {
        'order': [order],
        'order_products': order_products,
    }
    return render(request, 'store/order_success.html',context)







