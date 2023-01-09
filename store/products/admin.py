from django.contrib import admin

from products.models import ProductCategory, Product, Basket


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category')
    list_display_links = ('id', 'name',)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


# @admin.register(Basket)
# class BasketAdmin(admin.TabularInline):
#     list_display = ('user', 'product', 'quantity')
