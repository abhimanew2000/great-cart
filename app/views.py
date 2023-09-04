from django.shortcuts import render
from django.http import HttpResponse
from app.models import Product
# Create your views here.
def index(request):
    products = Product.objects.filter(is_available=True)[:8]
    context={
        'products':products,
    }
    return render(request,'index.html',context)
    





