from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.orders import Order

# Register your models here.
# here admin options


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


# it how the name of all categries in admin 
class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(Order)
