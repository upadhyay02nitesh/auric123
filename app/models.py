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
    ('T', 'Trending')
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
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

    def get_images(self):
        return self.images.all() # Fetch all associated images



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')




    def __str__(self):
        return f"Image for {self.product.title}" # Use the related Product title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    pandit = models.CharField(max_length=100)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    pincode = models.IntegerField(null=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255, default='Not provided')

    def __str__(self):
        return f"Booking by {self.name} on {self.booking_date} at {self.booking_time}"


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField()
    photo = models.ImageField(upload_to='review_photos/', null=True, blank=True)
   # created_at = models.DateTimeField(default=timezone.now)
   # photo=models.ImageField(upload_to='review_photo/', null=True, blank=True

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.title}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # One-to-one relationship with User
    name = models.CharField(max_length=200, blank=False) # Name is required
    mobile_number = models.CharField(max_length=15, blank=False) # Mobile number is required
    Gmail = models.EmailField(blank=False) # Email is required
    pincode = models.CharField(max_length=6, blank=False) # Use CharField to keep leading zeros in pincode
    state = models.CharField(max_length=100, default='Unknown', blank=False) # State is required
    district = models.CharField(max_length=100, default='Unknown', blank=False) # District is required
    address = models.CharField(max_length=255, default='Unknown', blank=False) # Address is required

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user_profile')
        ]

    def __str__(self):
        return f"{self.name} - {self.user.username}"


    def __str__(self):
        return str(self.id)

class Pandit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Link to a user
    name = models.CharField(max_length=200, null=True) # Name of the pandit
    specialty = models.CharField(max_length=100, null=True) # Area of expertise (e.g., Havan, Pooja)
    pincode = models.IntegerField(null=True)
    city = models.CharField(max_length=50, default="Unknown") # City the pandit is based in
    state = models.CharField(max_length=50, default="Unknown") # State the pandit is based in
    contact_number = models.CharField(max_length=15, null=True) # Pandit's contact number
    email = models.EmailField(null=True) # Pandit's email address

    def __str__(self):
        return self.name

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
    ('Pending','Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)



from django.db import models
from django.contrib.auth.models import User

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True) # Add this field
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', null=True)
    name = models.CharField(max_length=255, default='default_name', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # New fields for address-related data
    address = models.CharField(max_length=255, blank=True, null=True) # Address field
    pincode = models.CharField(max_length=10, blank=True, null=True) # Pincode field
    mobile_number = models.CharField(max_length=15, blank=True, null=True) # Mobile number field
    gmail = models.EmailField(max_length=255, blank=True, null=True) # Gmail field
    state = models.CharField(max_length=100, blank=True, null=True) # State field
    district = models.CharField(max_length=100, blank=True, null=True) # District field

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * (self.product.discounted_price or 0)

    # Optionally, you can define a method to return the full address:
    def full_address(self):
        return f"{self.address}, {self.district}, {self.state} - {self.pincode}"


class OrderItem(models.Model):
    razorpay_order_id = models.CharField(max_length=255, unique=True)
    order = models.ForeignKey(OrderPlaced, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price