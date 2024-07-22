from django.contrib import admin

# Register your models here.

from .models import *

class ImagesTublerinline(admin.TabularInline):
    model = Images

class TagTublerinline(admin.TabularInline):
    model = Tag

class SizeTublerinline(admin.TabularInline):
    model = Size

class Product_ColorTublerinline(admin.TabularInline):
    model = Product_Color

class ProdcutAdmin(admin.ModelAdmin):
    inlines = [ImagesTublerinline, TagTublerinline, Product_ColorTublerinline, SizeTublerinline] 

class Order_itemTublerinline(admin.TabularInline):
    model = Order_item

class OrderAdmin(admin.ModelAdmin):
    inlines = [Order_itemTublerinline]
    

admin.site.register(Categories)
admin.site.register(Filter_price)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Product, ProdcutAdmin)
admin.site.register(Images)
admin.site.register(Tag)
admin.site.register(Contact)
admin.site.register(Order, OrderAdmin)
admin.site.register(Order_item)
admin.site.register(Wishlist)
admin.site.register(Size)
admin.site.register(Product_Color)
admin.site.register(Cart1)
