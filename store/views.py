from django.shortcuts import render, get_object_or_404,redirect
from app.models import Product, Category
from carts.models import CartItem,Carts
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from app.models import ProductGallery
from django.db.models import Q

def store(request, cat_slug=None):
    categories = None
    products = None

    if cat_slug is not None:
        category = get_object_or_404(Category, cat_slug=cat_slug)
        products = Product.objects.filter(category=category, is_available=True)
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator=Paginator(products,3)
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

def product_detail(request, cat_slug, slug):
    try:
        category = get_object_or_404(Category, cat_slug=cat_slug)
        single_product = get_object_or_404(Product, category=category, slug=slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        is_accessory = single_product.category.title == "Accessories"  # Check if the product belongs to the "Accessory" category
        images = single_product.gallery_images.all() 

        search_query = request.GET.get('q')
        if search_query:
            matching_product = Product.objects.filter(title__icontains=search_query).first()
            if matching_product:
                return redirect('product_detail', category.cat_slug, matching_product.slug)



    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'is_accessory': is_accessory,
        'category': category,
        'images': images,
        

    }
    return render(request, 'store/product_detail.html', context)


def search_results(request):
    search_query = request.GET.get('q')
    
    if search_query:
        # Use your own logic to search for products by title
        products = Product.objects.filter(title__icontains=search_query)
        
        context = {
            'search_query': search_query,
            'products': products,
        }
        return render(request, 'store/product_detail.html', context)
    else:
        return redirect('store')