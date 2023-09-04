from django.contrib import admin
from .models import User,Address

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display =['username','email','bio']
admin.site.register(User,UserAdmin)
admin.site.register(Address)

