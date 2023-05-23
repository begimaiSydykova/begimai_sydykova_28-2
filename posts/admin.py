from django.contrib import admin

from .models import Product, Category, Reviews

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Reviews)
