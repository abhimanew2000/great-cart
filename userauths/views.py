from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User
from carts.models import Carts,CartItem
from orders.models import Order,OrderProduct
from django.views.decorators.cache import never_cache

import random
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from django.contrib import messages
import requests
# ----------------------------------Reset password imports-----------------------------------------------------------------------
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model, views as auth_views
from .models import Wallet
# ----------------------------------------------------------------------------------------------

from carts.views import _cart_id
from decimal import Decimal

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse



user = settings.AUTH_USER_MODEL
# def handlesignup(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
    # #     if form.is_valid():
    # #         new_user = form.save()
    # #         username = form.cleaned_data.get('username')
    # #         messages.success(request, f"Hey {username}, your account was successfully created.")
    # #         new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
    # #         login(request, new_user)
    # #         return redirect('app:index')
    # # else:
    # #     form = UserRegisterForm()
    # # context = {
    # #     'form': form,
    # # }
    # return render(request, 'userauths/signup.html', context)

def handlesignup(request): 
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            check_user = User.objects.filter(email=email).first()
            if check_user:
                messages.warning(request, "Email already exists")
                return redirect('handlesignup')
            
            request.session['registration_form_data'] = form.cleaned_data
            otp = random.randint(100000, 999999)
            request.session['otp'] = str(otp)
            send_mail(
                'OTP Verification',
                'Your OTP is ' + str(otp),
                'abhimanew2000@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('otp_verify')
    else:
    
        form = UserRegisterForm()
    return render(request, 'userauths/signup.html', {'form': form})




def otp_verify(request):
    if 'otp' in request.session: 
        if request.method == 'POST':
            otp = request.POST.get('otp')
            if otp == request.session.get('otp'):
                form_data = request.session.get('registration_form_data')
                form = UserRegisterForm(form_data)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.username = user.email.split("@")[0]
                    user.is_active = True
                    user.save()
                    messages.success(request, 'Registration Successful')
                    request.session.flush()
                    return redirect('handlelogin')
                else:
                    messages.error(request, 'Invalid form data')
                    return redirect('handlesignup')
            else:
                messages.error(request, 'Invalid OTP')
                return redirect('otp_verify')
        return render(request, 'userauths/otpverify.html')
    else:
        return redirect('handlesignup')



def handlelogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, f"User with {email} does not exist")

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_blocked==False:
            if user.is_superuser:
                login(request, user)
                messages.success(request, "Admin login successful")
                return redirect('admin_panel')
            try:
                cart=Carts.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)
                    # getting product variation by cart_id
                    product_variation=[]
                    for item in cart_item:
                        variation=item.variation.all()
                        product_variation.append(list(variation))

                     # get the cartitems from the user to access his product variation
                    cart_item=CartItem.objects.filter(user=user)
                    ex_var_list=[]
                    id=[]
                    for item in cart_item:
                        existing_variation=item.variation.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index=ex_var_list.index(pr)
                            item_id= id [index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity +=1
                            item.user=user
                            item.save()

                        else:
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()
            except:
                pass
            login(request, user)
            messages.success(request, f"You are logged in")
            url = request.META.get("HTTP_REFERER")
            # the above line will grab previous url
            try:
                query=requests.utils.urlparse(url).query
                print('query-->',query)
                # next=cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                # x.split is splitting the = line
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('index')

        else:
            messages.warning(request, f"User does not exist")

    return render(request, "userauths/handlelogin.html")


@never_cache
def handlelogout(request):
    logout(request)
    
    return redirect('index')
# @login_required(login_url='handlelogin')
# def dashboard(request):
#     # Retrieve orders for the current user
#     orders = Order.objects.filter(user=request.user)
    
#     context = {
#         'orders': orders,
#     }
#     return render(request, 'userauths/dashboard.html', context)

def dashboard(request):
    # Retrieve orders for the current user
    orders = Order.objects.filter(user=request.user)

    # Attach the ordered products for each order
    for order in orders:
        order.order_products = OrderProduct.objects.filter(order=order)
    context = {
        'orders': orders,

    }
    
    return render(request, 'userauths/dashboard.html', context)

def view_order(request, order_id):
    print(order_id)
    order = get_object_or_404(Order, id=order_id)
    order_products = OrderProduct.objects.filter(order=order)

    context = {
        'order': order,
        'order_products': order_products,
    }

    return render(request, 'userauths/view_order.html', context)

def cancel_order_product(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if order.status != 'Cancelled':
        order.status = 'Cancelled'
        canceled_amount = Decimal(str(order.order_total))
        order.save()

        # Increase view_count for each OrderProduct
        order_products = OrderProduct.objects.filter(order=order)
        for order_product in order_products:
            product = order_product.product
            product.view_count += order_product.quantity
            product.save()

        user = request.user
        user_wallet, created = Wallet.objects.get_or_create(user=user)
        user_wallet.balance += canceled_amount
        user_wallet.save()

    return redirect('view_order', order_id=order.id)



# --------------------------Reset password view--------------------------------------------------
User = get_user_model()

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Generate password reset token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Build the reset link URL
            reset_url = f"{request.scheme}://{request.get_host()}/userauths/reset-password-confirm/{uid}/{token}/"

            # Send the password reset email
            subject = 'Password Reset'
            message = render_to_string('userauths/reset_password_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, 'Password reset link sent to your email.')
            return redirect('handlelogin')
        else:
            messages.error(request, 'User with this email does not exist.')
            return redirect('reset_password')

    return render(request, 'userauths/reset_password.html')


def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode URLsafe base64 and convert to string
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Password reset successful. You can now log in with your new password.')
                return redirect('handlelogin')
        else:
            form = SetPasswordForm(user)

        return render(request, 'userauths/reset_password_confirm.html', {'form': form})
    else:
        messages.error(request, 'Invalid password reset link. Please try again.')
        return redirect('handlelogin')
    
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

@login_required(login_url='handlelogin')
def profile_information(request):
    if request.method == 'POST':
        if 'change_password' in request.POST:
            # Handle password change form submission
            current_password = request.POST.get('current_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            user = request.user
            if user.check_password(current_password):
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "Password changed successfully.")
                else:
                    messages.error(request, "New passwords do not match.")
            else:
                messages.error(request, "Incorrect current password.")
        else:
            # Handle profile information update form submission
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_number = request.POST.get('phone_number')

            user = request.user
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.save()

            messages.success(request, "Profile updated successfully.")
            
        return redirect('profile_information')
    user_wallet, created = Wallet.objects.get_or_create(user=request.user)
    context = {
        'user': request.user,
        'user_wallet': user_wallet,
    }
    return render(request, 'userauths/profile_information.html', context)

# --------------------------manage addresses---------------------------------------
from .models import Address
def manage_addresses(request):
    if request.method == 'POST':
        # Handle the form submission to add a new address
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')

        # Create a new Address object and save it to the database
        address = Address(
            first_name=first_name,
            last_name=last_name,

            phone=phone,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            postal_code= postal_code,
            country=country,
            user=request.user  # Assuming you have implemented authentication
        )
        address.save()

        # Redirect to the manage addresses page after adding the new address
        return redirect('manage_addresses')

    else:
        # Retrieve the existing addresses for the current user
        addresses = Address.objects.filter(user=request.user)

        context = {
            'addresses': addresses
        }
        return render(request, 'userauths/manage_addresses.html', context)
def delete_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id)
        address.delete()
        # You can add a success message here if you want
    except Address.DoesNotExist:
        # Address with the given ID not found, you can handle this error accordingly
        pass
    return redirect('manage_addresses')


from django.shortcuts import redirect, render, get_object_or_404
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        # Get the updated values from the POST data
        address.first_name = request.POST.get('first_name')
        address.last_name = request.POST.get('last_name')
        address.email = request.POST.get('email')
        address.phone = request.POST.get('phone')
        address.address_line_1 = request.POST.get('address_line_1')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.country = request.POST.get('country')
        address.save()
        # You can add a success message here if you want
        return redirect('manage_addresses')

    context = {
        'address': address,
        'address_id': address_id,
    }
    return render(request, 'userauths/edit_address.html', context)

@login_required(login_url='handlelogin')
def add_address(request):
    if request.method == 'POST':
        # Get the form fields from the POST data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')

        # Get the logged-in user
        user = request.user

        # Create a new Address object and set the user before saving
        address = Address(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address_line_1=address_line_1,
            # address_line_2=address_line_2,
            city=city,
            state=state,
            country=country
        )
        address.save()

        # Redirect back to the manage_addresses page
        return redirect('manage_addresses')

    return render(request, 'userauths/add_address.html')



def invoice_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_products = OrderProduct.objects.filter(order=order)
    
    context = {
        'order': order,
        'order_products': order_products,
    }
    
    return render(request, 'userauths/invoice.html', context)

def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_products = OrderProduct.objects.filter(order=order)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Invoice - Order ID: {order.id}", styles['Heading1']))
    elements.append(Paragraph(f"Order Date: {order.created_at}", styles['Normal']))
    elements.append(Paragraph(f"Total Amount: {order.order_total}", styles['Normal']))
    elements.append(Paragraph(f"Status: {order.status}", styles['Normal']))
    
    # Display user details
    user = order.user
    elements.append(Paragraph(f"User: {user.username}", styles['Normal']))
    elements.append(Paragraph(f"Email: {user.email}", styles['Normal']))
    elements.append(Paragraph(f"First Name: {user.first_name}", styles['Normal']))
    elements.append(Paragraph(f"Last Name: {user.last_name}", styles['Normal']))
    
    data = [['Product', 'Quantity', 'Price', 'Variation']]
    for item in order_products:
        data.append([item.product.title, item.quantity, item.product_price, item.variation])
    
    table = Table(data, colWidths=[200, 50, 75, 150])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    elements.append(table)
    doc.build(elements)

    return response













