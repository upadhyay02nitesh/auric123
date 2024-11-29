from django.contrib import admin
from .models import Product, Customer, OrderPlaced, Cart, Review, Booking

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(OrderPlaced)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(Booking)
