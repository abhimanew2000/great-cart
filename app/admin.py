from django.contrib import admin
from app.models import Product,Cart,CartProduct,Category,ProductGallery,Variation
# Register your models here.
from .models import Variation


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable=('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(Variation, VariationAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)

admin.site.register(Category)
admin.site.register(ProductGallery)
