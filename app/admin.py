from django.contrib import admin
from .models import Pandit, Product, Customer, OrderPlaced, Cart, Review, Booking,ProductImage

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(OrderPlaced)

admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(Booking)
admin.site.register(Pandit)
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4  # Allows up to five images (1 existing + 4 extra)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(ProductImage) 
