from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Choices for category and state
CATEGORY_CHOICES = (
    ('M', 'Pooja Samgri'),
    ('H', 'Havan Samagri'),
    ('S', 'Spices'),
    ('J', 'Jadi Booti'),
    ('JM', 'Jap Mala'),
    ('I', 'Idols'),
    ('R', 'Roodraksh'),
)

STATE_CHOICES = (
    ('Andaman & Nicobar Islands', 'Andman & Nicobar Islands'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Dadra & Nagar Haveli', 'Dadra & Nagar Haveli'),
    ('Daman and Diu', 'Daman and Diu'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu & Kashmir', 'Jammu & Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Goa', 'Goa'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bengal', 'West Bengal'),
    ('Uttarakhand', 'Uttarakhand'),
    ('Tripura', 'Tripura'),
    ('Telangana', 'Telangana'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Odisha', 'Odisha'),
    ('Rajasthan', 'Rajasthan'),
    ('Mizoram', 'Mizoram'),
)

class Product(models.Model):
    title = models.CharField(max_length=100, null=True)
    selling_price = models.FloatField(null=True)
    discounted_price = models.FloatField(null=True)
    description = models.TextField(null=True)
    brand = models.CharField(max_length=100, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2, null=True)
    FAQ = models.TextField(null=True)
    Product_Analysis = models.URLField(null=True)
    product_image = models.ImageField(upload_to='product_images', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} on {self.booking_date}"


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField()
    photo = models.ImageField(upload_to='review_photos/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.title}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Use OneToOneField
    name = models.CharField(max_length=200, null=True)
    locality = models.CharField(max_length=200, default="Unknown")
    city = models.CharField(max_length=50, default="Unknown")
    zipcode = models.IntegerField(null=True)
    mobile_number = models.CharField(max_length=15, null=True)
    Gmail = models.EmailField(null=True)
    state = models.CharField(choices=STATE_CHOICES, max_length=50, default="Unknown")

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True)
    name = models.CharField(max_length=255, default='default_name', null=True)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)



class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)  # Add this field
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255, default='default_name', null=True)


    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * (self.product.discounted_price or 0)
class OrderItem(models.Model):
    order = models.ForeignKey(OrderPlaced, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price
