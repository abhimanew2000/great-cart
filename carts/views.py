from django.shortcuts import render, redirect,get_object_or_404
from app.models import Product
from .models import Carts, CartItem
from django.core.exceptions import ObjectDoesNotExist
from app.models import Variation
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from userauths.models import Address
from orders.models import Order,OrderProduct,Payment,Razorpay_Order
import razorpay
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
import hmac
import hashlib
import logging
from .models import Wishlist,Coupon
from django.utils import timezone
from django.contrib import messages
from datetime import date
from orders.constant import PaymentStatus
from django.views.decorators.cache import never_cache

from django.views.decorators.csrf import csrf_exempt
import razorpay
from project.settings import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET,
)
from django.views.decorators.csrf import csrf_exempt
import json
from django.template.loader import render_to_string


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user=request.user
    product = Product.objects.get(id=product_id)
    
    # if user is authenticated
    if current_user.is_authenticated:
        product_variation=[]
        if request.method=="POST":
            for item in request.POST:
                key = item
                value=request.POST[key]
            try:
                variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                print(variation)
                product_variation.append(variation)
            except:
                pass

        
        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,user=current_user)
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)
            if product_variation in ex_var_list:
                # increase cartitem quantity
                index=ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity +=1
                item.save()
            else:
                # create new cartitem
                item=CartItem.objects.create(product=product,quantity=1,user=current_user)
                if len(product_variation) >0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
            # cart_item.quantity +=1
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            

            if len(product_variation) >0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
                cart_item.save()
        
        return redirect('cart')
    #if user is not authenticated 
    else:
        product_variation=[]
        if request.method=="POST":
            for item in request.POST:
                key = item
                value=request.POST[key]
            try:
                variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                print(variation)
                product_variation.append(variation)
            except:
                pass

        try:
            cart = Carts.objects.get(cart_id=_cart_id(request))
        except Carts.DoesNotExist:
            cart = Carts.objects.create(cart_id=_cart_id(request))

        cart.save()
        is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()


        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(product=product,cart=cart)

            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)
            if product_variation in ex_var_list:
                # increase cartitem quantity
                index=ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity +=1
                item.save()


            else:
                # create new cartitem
                item=CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) >0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
            # cart_item.quantity +=1
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            

            if len(product_variation) >0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
                cart_item.save()
        
        return redirect('cart')

   
    

   

def remove_cart(request,product_id,cart_item_id):
    product=get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart=Carts.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity >1:
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')
    
  
def remove_cart_item(request, product_id,cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
    else:
        cart=Carts.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
  

def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grandtotal=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Carts.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.selling_price*cart_item.quantity)
            quantity += cart_item.quantity
        tax=(2* total)/100
        grandtotal =total+ tax
    except ObjectDoesNotExist:
        pass


    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grandtotal':int(grandtotal),
    }
    print(context,"22222222222")
    return render(request, 'store/cart.html', context)


RAZORPAY_KEY_ID = 'rzp_test_4o90y50Nv7s1jR'
RAZORPAY_KEY_SECRET = 'nlmYaIYmAyx29rc3BUZSmDRu'

@login_required(login_url='handlelogin')
def checkout(request,grandtotal,total=0,quantity=0,cart_items=None,):
    try:
        checkaddress=Address.objects.filter(user=request.user)
    except:
        return redirect('add_address')
    if not checkaddress:
        return redirect('add_address')

    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user, is_active=True)
    cart_count = cart_items.count()
    if cart_count <= 0:
        print('hhhhhhdddddddddddd')
        return redirect('store')
    
    coupon_code = request.POST.get('coupon_code')
    print('coupon_code',coupon_code)
    # if coupon_code:
    #     try:
    #         coupon = Coupon.objects.get(code=coupon_code, is_active=True, expiration_date__gte=date.today())
    #         coupon_discount = (coupon.discount / 100) * grand_total
    #         final_total -= coupon_discount
    #         print('final total',final_total)
    #     except Coupon.DoesNotExist:
    #         pass  # Handle invalid coupon code
    
    # -------------------coupon--------------------------
   
    print(grandtotal)

    grand_total = grandtotal
    for cart_item in cart_items:
        print(cart_item.quantity)
        print(cart_item.product.selling_price)

        grand_total += cart_item.product.selling_price* cart_item.quantity
    tax = (2 * grand_total) / 100
    grand_total += tax
    
    coupon_discount = 0
    final_total = grandtotal

    print('grand_total',grandtotal)
    addresses = Address.objects.filter(user=current_user)


 
    if request.method == 'POST':     
        print('helooooooooooooooo') 
        selected_address_id = request.POST.get('selected_address')
        coupon_code = request.POST.get('coupon_code')
        action=request.POST.get('action')


        payment_id=request.POST.get('payment_id')
        print('paymentid',payment_id)
        print('selected address is :', selected_address_id) 
        # grand_total = int(request.POST.get('grand_total', 0))
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True, expiration_date__gte=date.today())
                coupon_discount = (coupon.discount / 100) * grandtotal
                final_total -= coupon_discount
                print('final total',final_total)
                print('coupon_code is ...',coupon_code)

            except Coupon.DoesNotExist:
                pass 
        try:
            selected_address = Address.objects.get(pk=int(selected_address_id), user=request.user)
            print('selected add :', selected_address_id) 

        except Address.DoesNotExist:
            return redirect('store')  # Redirect to store page if selected address is not found
            
            
            
       
        summary_context = {
            'selected_address': selected_address,
            'cart_items': cart_items,
            'coupon_discount': coupon_discount,
            'final_total': final_total,
            
        }

        return render(request, 'store/proceed_to_pay.html', summary_context)

 
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax':tax,
        'grandtotal':int(grandtotal),
        'addresses': addresses,
        # 'final_total': final_total,
        'final_total': grand_total,  # Pass the calculated grand_total to the template

        
        
    }


    return render(request,'store/checkout.html',context)



def success_view(request):
    order_id = request.session.get('order_id')  # Change this based on your logic
    order = get_object_or_404(Order, id=order_id)
    order_products = OrderProduct.objects.filter(order=order)

    context = {
        'order': order,
        'order_products': order_products,
    }
    return render(request, 'store/success.html')
import razorpay
import logging








# -------------------------------wishlist---------------------------------------------------
def add_to_wishlist(request, product_id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=product_id)
        current_user = request.user

        # You need to adjust this part based on how you retrieve variations
        variation_id = request.POST.get('variation_id')  # Replace 'variation_id' with the actual field name
        print("Variation ID from form:", variation_id) 
        if variation_id:
            variation = Variation.objects.get(id=variation_id)
        else:
            variation = None

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=current_user, product=product, variation=variation
        )

        return redirect('wishlist')  # Redirect to the wishlist view
    else:
        return redirect('login')
def wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        wishlist_items = Wishlist.objects.filter(user=user)
        context = {'wishlist_items': wishlist_items}
        return render(request, 'store/wishlist.html', context)
    else:
        return redirect('handlelogin')
    
def add_to_cart_from_wishlist(request, wishlist_item_id):
    print("wishlist",wishlist_item_id)
    if request.method == 'POST':
        print("wishlist",wishlist_item_id)
        wishlist_item = get_object_or_404(Wishlist, id=wishlist_item_id)
        product = wishlist_item.product
        user = request.user
        variation = wishlist_item.variation

        # Add the product to the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart_id=_cart_id(request),
            product=product,
            user=user,
            variation=variation
        )

        # Remove the item from the wishlist
        wishlist_item.delete()

        return redirect('cart')
    else:
        return redirect('wishlist')

def remove_from_wishlist(request, wishlist_item_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_item_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist')


def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        grand_total = float(request.POST.get('grand_total'))
        print("Coupon Code:", coupon_code)
        print("Grand Total:", grand_total)

        coupon = get_object_or_404(Coupon, code=coupon_code, is_active=True, expiration_date__gte=date.today())
        coupon_discount = (coupon.discount / 100) * grand_total
        final_total = grand_total - coupon_discount
        
        response_data = {
            'status': 'success',
            'coupon_discount': coupon_discount,
            'final_total': final_total,
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error'})
    

def proceed_to_pay(request, grandtotal):
    print("get inside",grandtotal)
    selected_address_id = request.session.get('selected_address_id')
    tax=request.POST.get('tax')
    selected_address = get_object_or_404(Address, id=selected_address_id)

    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user, is_active=True)

    # Calculate coupon_discount and final_total based on coupon code (similar to checkout view)
    coupon_code = request.POST.get('coupon_code')
    coupon_discount = 0

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True, expiration_date__gte=date.today())
            coupon_discount = (coupon.discount / 100) * grandtotal
        except Coupon.DoesNotExist:
            pass

    final_total = grandtotal - coupon_discount

    # Create the order
    order = Order.objects.create(
        user=current_user,
        selected_address=selected_address,
        order_total=final_total,
        # tax=calculate_tax(grandtotal),  # Replace with your tax calculation logic
        status='New',
        discount=coupon_discount,  # Save coupon discount in the order's discount field
    )
    print(order.order_total,"tttttttttttttttttttttttttttttttttttttttt")
    order_id = order.id
    print(order_id,"orderrrrrrrrrrrr")
    # Other context variables needed for the template
    context = {
        'selected_address': selected_address,
        'cart_items': cart_items,
        'coupon_discount': coupon_discount,
        'final_total': final_total,
        'order': order.id,  # Pass the order object to the template
    }

    return render(request, 'store/proceed_to_pay.html', context)

def place_order(request):
    if request.method == 'POST':
        action=request.POST.get('action')
        print(action,'actionnnnnnn')
        selected_address_id = request.POST.get('selected_address')
        print(selected_address_id,"bbbbbbbbb")
        final_total=request.POST.get('final_total')
        print(final_total,"fffffffffffff")
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)



        if action=="Cash on Delivery":
            selected_address = get_object_or_404(Address, id=selected_address_id)

            order = Order.objects.create(
            user=request.user,
            selected_address=selected_address,
            order_total=final_total,
            status='New',  # Set the status to 'New' for a new order
            paymenttype="Cash On delivery",
            
        )
            for cart_item in cart_items:
                for variation in cart_item.variation.all():  # Loop through all variations for this cart item
                    OrderProduct.objects.create(
                            order=order,
                            user=request.user,
                            product=cart_item.product,
                            variation=variation,  # Assign the specific variation
                            quantity=cart_item.quantity,
                            product_price=cart_item.product.selling_price,
                        )
                cart_item.product.view_count -= cart_item.quantity
                cart_item.product.save()
            
            cart_items.delete()
            return redirect("order_success",id=order.id)


        if action == "Pay with Razorpay":

            selected_address = get_object_or_404(Address, id=selected_address_id)
            amount = str(final_total)
            name=selected_address.first_name
            amount = float(amount)
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create(
                {"amount":int(amount)*100,"currency":"INR","payment_capture":"1"}
            )
            orders = Razorpay_Order.objects.create(
                    name=selected_address.first_name, amount=amount, provider_order_id=razorpay_order["id"]
                    )
            orders.save()
            order = Order.objects.create(
            user=request.user,
            selected_address=selected_address,
            order_total= amount,
            status='New',  # Set the status to 'New' for a new order
            paymenttype="Razorpay",
            
            
        )
            for cart_item in cart_items:
                for variation in cart_item.variation.all():  # Loop through all variations for this cart item
                    OrderProduct.objects.create(
                            order=order,
                            user=request.user,
                            product=cart_item.product,
                            variation=variation,  # Assign the specific variation
                            quantity=cart_item.quantity,
                            product_price=cart_item.product.selling_price,
                        )
                cart_item.product.view_count -= cart_item.quantity
                cart_item.product.save()
            bulk_order_id=order.id
            cart_items.delete()
            current_order = bulk_order_id
            current_user = request.user
            print(current_user,"current_userrrrrrrrrr",current_order)


            return render(
                request,
                "store/payment.html",
                {
                "callback_url": "http://" + "www.abhimanew.live" + "/carts/callback/?current_order={}".format(current_order),
                    "razorpay_key": RAZORPAY_KEY_ID,
                    "orders": orders,
                    "final_total": final_total,

                },
            )
        
        




        
        else:
            pass
            print("pass")
    return render(request, "store/payment.html")



# @csrf_exempt
# def callback(request):
#     print('enter to callback function')
#     current_user = request.GET.get("current_user")   
#     bulk_order_id = request.GET.get("current_order")
#     print("current_userrrrrrrrrrrr",current_user)
    

#     current_order = Order.objects.filter(id = bulk_order_id)

#     def verify_signature(response_data):
#         client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
#         print(client,'ccccccccccccccccccccc')
#         return client.utility.verify_payment_signature(response_data)
#     print(request,"request")
#     print(request.POST,"requst.post")
#     # signature_id = request.POST.get("razorpay_signature", "")
#     # signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE', '')
#     # print('signature is signature',signature)

#     print(signature_id,"singature iddddddddddddddddd",request)
#     if "razorpay_signature" in request.POST:
#         payment_id = request.POST.get("razorpay_payment_id", "")
#         provider_order_id = request.POST.get("razorpay_order_id", "")
#         print(provider_order_id,"providerrrrrrrrrrrrrrrr")
#         signature_id = request.POST.get("razorpay_signature", "")

#         order = Razorpay_Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.signature_id = signature_id
#         order.save()
#         if  verify_signature(request.POST):
#             order.status = PaymentStatus.SUCCESS
#             order.save()
#             print("success")
#             current_order.update(payment_status = "Paid")
#             print(current_order,"status")
#             # cart_items.delete()
#             # return render(request, "orders/order_summery.html", context={"status": order.status})
#             # return redirect('order_summery', bulk_order_id=bulk_order_id)
#             return redirect("order_success",id=bulk_order_id)

        
#         else:
#             order.status = PaymentStatus.FAILURE
#             order.save()
#             current_order.delete()
#             print("failed")
#             return render(request, "orders/order_failed.html")
        
#     else:
#         print(request.POST.get("error[metadata]"),"heloooooo")
  
#         payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
#         provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
#             "order_id"
#         )
#         try:
#             order = Razorpay_Order.objects.get(provider_order_id=provider_order_id)
#             order.payment_id = payment_id
#             order.status = PaymentStatus.FAILURE
#             order.save()
#             current_order.delete()
#             print("else failed")
#             return render(request, "orders/order_failed.html")
#         except:
#             return render(request, "orders/order_failed.html")




@csrf_exempt      
def callback(request):
    bulk_order_id = request.GET.get("current_order")
    print(bulk_order_id,"bbbbbbbb")
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)
        print('11111111111111111111111111111')
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        print("Provider Order ID:", provider_order_id)
        signature_id = request.POST.get("razorpay_signature", "")
        print('signature idddddd',signature_id)
        orders = Razorpay_Order.objects.get(provider_order_id=provider_order_id)
        orders.payment_id = payment_id
        orders.signature_id = signature_id
        orders.save()
        if verify_signature(request.POST):
            orders.status = PaymentStatus.SUCCESS
            orders.save()
            return redirect('order_success',bulk_order_id)
        else:
            orders.status = PaymentStatus.FAILURE
            orders.save()
            return render(request, "store/payment_failure.html", context={"status": orders.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        orders = Razorpay_Order.objects.get(provider_order_id=provider_order_id)
        orders.payment_id = payment_id
        orders.status = PaymentStatus.FAILURE
        orders.save()
        return render(request, "payment_success.html", context={"status": orders.status})

def ordersuccess(request,id):
    
    return render(request, "store/order_success.html")        

    
# @never_cache
# def order_summery(request, bulk_order_id):

#     cart_items = CartItem.objects.all()
#     for cart in cart_items:
#         if cart.variant.variant_stock > 0:
#             cart.delete()
#         else:
#             pass 
#     orders = Order.objects.filter(bulk_order_id = bulk_order_id)
#     print(bulk_order_id,"got it bulk order id")
#     order_user = request.user
#     # coupon_amount = orders.coupon.discount_price
#     # total_amount = orders.total_amount+coupon_amount
#     context = {
#     "orders":orders,
#     "user":order_user,
#     # "total_amount":total_amount,
#     }
#     return render(request, "orders/order_summery.html",context)