from django.urls import path
from store import views  # Update the import statement here

urlpatterns = [
    path('', views.store, name='store'),  # Use the 'store' view from the correct import
    path('<slug:cat_slug>/', views.store, name='products_by_category'),  
    path('<slug:cat_slug>/<slug:slug>/', views.product_detail, name='products_detail'),  
    # path('search/', views.search, name='search'),  
    path('search/', views.search_results, name='search_results'),


]
