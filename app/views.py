import hmac
import logging
from django.shortcuts import render,redirect
from django.views import View
import requests
from .models import Customer, OrderItem, Pandit,Product,Cart,OrderPlaced,Review,Booking
from.forms import CustomerRegistrationForm,CustomerProfileForm, PanditForm
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.contrib.auth import logout
import datetime 
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
import hashlib
import datetime


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Review,OrderPlaced
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

@login_required
def submit_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        comment = request.POST.get('comment')
        photo = request.FILES.get('photo')

        # Create the review
        Review.objects.create(
            product=product,
            user=request.user,
            comment=comment,
            photo=photo
        )

        # Add a success message
        messages.success(request, "Thanks for submitting your review!")

        # Redirect back to the product detail page
        return redirect('product-detail', pk=product.id)

    # If the request is not POST
    return redirect('product-detail', pk=product_id)

@login_required
def get_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).select_related('user')

    reviews_data = [
        {
            'username': review.user.username,
            'comment': review.comment,
            'created_at': review.created_at.strftime('%Y-%m-%d %H:%M'),
            'photo_url': review.photo.url if review.photo else None
        }
        for review in reviews
    ]

    return JsonResponse({'reviews': reviews_data})


def home(request):
 return render(request, 'app/home.html')
from django.core.mail import send_mail, BadHeaderError
from django.utils.html import format_html
from django.core.exceptions import ObjectDoesNotExist
@login_required
def add_pandit(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        specialty = request.POST.get('specialty')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')

        # Basic validation
        if not name or not specialty or not city or not state or not contact_number or not email:
            messages.error(request, "All fields are required!")
            return render(request, 'app/add_pandit.html')

        try:
            # Check if the email is already registered
            existing_pandit = Pandit.objects.filter(email=email).first()
            if existing_pandit:
                messages.error(
                    request,
                    f"Email {email} is already registered. Please use a different email or register with a different name."
                )
                return render(request, 'app/add_pandit.html')

            # Create a new Pandit object
            pandit = Pandit(
                user=request.user,
                name=name,
                specialty=specialty,
                city=city,
                state=state,
                pincode=pincode,
                contact_number=contact_number,
                email=email
            )
            pandit.save()

            # Send email notification
            try:
                # Email content
                subject = f"Registration Successful: Welcome, Pandit {pandit.name}!"
                html_message = format_html(f"""
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px;">
                        <h2 style="color: #007bff; text-align: center;">Pandit Registration Successful</h2>
                        <p style="color: #333;">Hello <strong>{pandit.name}</strong>,</p>
                        <p>Your registration as a Pandit has been successfully completed. Below are your details:</p>
                        <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
                            <tr><td style="padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9;"><strong>Specialty:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{pandit.specialty}</td></tr>
                            <tr><td style="padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9;"><strong>City:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{pandit.city}</td></tr>
                            <tr><td style="padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9;"><strong>State:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{pandit.state}</td></tr>
                            <tr><td style="padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9;"><strong>Pincode:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{pandit.pincode}</td></tr>
                            <tr><td style="padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9;"><strong>Contact Number:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{pandit.contact_number}</td></tr>
                            <tr><td style="padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9;"><strong>Email:</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{pandit.email}</td></tr>
                        </table>
                        <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
                        <p>If you have any questions, feel free to contact us:</p>
                        <p><strong>Email:</strong> auricmart@gmail.com</p>
                        <p><strong>Telephone:</strong> +91-6268944329 / +91-6264534556</p>
                        <p style="text-align: center; margin-top: 20px;">Thank you for joining <strong>Auric Pandit</strong>!</p>
                    </div>
                """)
                from_email = 'niteshupa6@gmail.com'
                recipient_list = [pandit.email]

                # Send the email
                send_mail(subject, '', from_email, recipient_list, html_message=html_message)
                messages.success(request, "Pandit added successfully and email sent!")
            except BadHeaderError:
                messages.error(request, "Invalid header found.")
            except Exception as e:
                messages.error(request, f"Email sending failed: {str(e)}")

            return redirect('pandit')
        except Exception as e:
            messages.error(request, f"Error adding Pandit: {str(e)}")

    return render(request, 'app/add_pandit.html')


def about(request):
 return render(request, 'app/about.html')

@login_required
def book_schedule(request):
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        category = request.POST.get('category')
        pandit = request.POST.get('pandit')
        booking_date = request.POST.get('date')
        booking_time = request.POST.get('time')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        api_url = f"https://api.postalpincode.in/pincode/{pincode}"

        # Validate pincode, state, and city
        try:
            response = requests.get(api_url)
            response_data = response.json()
            
            if response_data[0]['Status'] == 'Success':
                # Extract State and City from the API response
                post_office = response_data[0]['PostOffice'][0]
                if post_office['State'] != state or post_office['District'] != city:
                    messages.error(request, "Pincode, state, and city do not match. Please check your inputs.")
                    return render(request, 'app/pandit.html', {'form_data': request.POST})
            else:
                messages.error(request, "Invalid pincode. Please enter a valid pincode.")
                return render(request, 'app/pandit.html', {'form_data': request.POST})
        except Exception as e:
            messages.error(request, f"Error validating pincode: {str(e)}")
            return render(request, 'app/pandit.html', {'form_data': request.POST})

        # Convert the date and time to proper formats
        try:
            if not booking_date or not booking_time:
                raise ValueError("Booking date and time are required.")
            
            # Convert the date and time to proper formats
            booking_date = datetime.datetime.strptime(booking_date, '%Y-%m-%d').date()
            booking_time = datetime.datetime.strptime(booking_time, '%H:%M').time()
        except ValueError as e:
            messages.error(request, f"Invalid date or time format: {str(e)}. Please enter valid values.")
            return render(request, 'app/pandit.html', {'form_data': request.POST})

        # Create a new booking entry
        try:
            Booking.objects.create(
                user=request.user,
                name=name,
                category=category,
                pandit=pandit,
                booking_date=booking_date,
                booking_time=booking_time,
                pincode=pincode,
                state=state,
                city=city,
                address=address
            )
            messages.success(request, "Your booking has been successfully recorded!")
            return redirect('pandit')  # Adjust this if you need to go somewhere else after success
        except Exception as e:
            messages.error(request, f"Error creating booking: {str(e)}")
            return render(request, 'app/pandit.html', {'form_data': request.POST})

    return render(request, 'app/pandit.html')  # Ensure the form is rendered correctly
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'app/bookings.html', {'bookings': bookings})

from django.shortcuts import render
from .models import Product

def search_view(request):
    query = request.GET.get('q')
    
    # Perform the search only if query is provided
    if query:
        results = Product.objects.filter(title__icontains=query)  # case-insensitive search
    else:
        results = []  # Empty list if no query
    
    return render(request, 'app/search_results.html', {'query': query, 'results': results})

class ProductDetailView(View):
    def get(self,request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id)&
            Q(user=request.user)).exists()

        return render(request,'app/productdetail.html',{'product': product,
        'item_already_in_cart': item_already_in_cart})
def pandit(request):
 return render(request,'app/pandit.html')
def pandit(request):
 return render(request,'app/pandit.html')
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            category = form.cleaned_data['category']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Email 1: Admin Notification
            admin_email_subject = f"Contact Form Submission: {subject} - {category}"
            admin_email_message = (
                f"<html>"
                f"<body>"
                f"<div style='border: 1px solid #ddd; padding: 20px; border-radius: 10px; font-family: Arial, sans-serif; width: 80%; margin: auto; background-color: #ffffff;'>"
                f"<h3 style='text-align: center; color: #4CAF50;'>New Contact Form Submission</h3>"
                f"<p><strong>From:</strong> {first_name} {last_name} ({email})</p>"
                f"<p><strong>Country:</strong> {country}</p>"
                f"<p><strong>Category:</strong> {category}</p>"
                f"<p><strong>Message:</strong><br>{message}</p>"
                f"<hr style='border: 1px solid #ddd;'>"
                f"<p style='font-size: 0.9em; text-align: center; color: #555;'>This message was automatically generated from the contact form on the website.</p>"
                f"</div>"
                f"</body>"
                f"</html>"
            )

            send_mail(
                admin_email_subject,
                "",  # Empty plaintext content
                "niteshupa6@gmail.com",  # Sender email
                ["niteshupa6@gmail.com"],  # Admin email
                fail_silently=False,
                html_message=admin_email_message  # Include HTML content
            )

            # Email 2: User Welcome Message
            user_email_subject = "Welcome to AuricMart!"
            user_email_message = (
                f"<html>"
                f"<body>"
                f"<div style='border: 1px solid #ddd; padding: 20px; border-radius: 10px; font-family: Arial, sans-serif; width: 80%; margin: auto; background-color: #f9f9f9;'>"
                f"<h2 style='color: #4CAF50;'>Welcome to AuricMart, {first_name} {last_name}!</h2>"
                f"<p>Thank you for reaching out to AuricMart, your trusted divine selling partner. We’re thrilled to connect with you!</p>"
                f"<p>Our team will get back to you shortly if necessary. Meanwhile, feel free to explore our services or contact us for any questions.</p>"
                f"<hr>"
                f"<p style='font-size: 0.9em;'>© 2024 AuricMart. All rights reserved.<br>"
                f"123 Market Street, Ujajin, India<br>"
                f"Phone: +91-6260144580 | Email: auricmart37@gmail.com</p>"
                f"</div>"
                f"</body>"
                f"</html>"
            )
            send_mail(
                user_email_subject,
                "",  # Empty plaintext content
                "niteshupa6@gmail.com",  # Sender email
                [email],  # User's email
                fail_silently=False,
                html_message=user_email_message  # Include HTML content
            )

            # Redirect to success page
            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'app/contact.html', {'form': form})



def contact_success(request):
    return render(request, 'app/contact_success.html')





def plus_cart(request):
    if request.method=='GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user ==request.user]
        for p in cart_product:

            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount      

        data={

            'quantity':c.quantity,
            'amount': amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)  # Debugging log
        
        try:
            # Retrieve the cart item for the given product and user
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            
            # Decrease the quantity
            cart_item.quantity -= 1

            if cart_item.quantity <= 0:
                # Remove the item from the cart if quantity is 0
                cart_item.delete()
                message = 'Item removed from cart'
            else:
                # Save the updated quantity
                cart_item.save()
                message = 'Item quantity updated'

            # Recalculate the total amounts
            amount = 0.0
            shipping_amount = 70.0
            cart_products = [p for p in Cart.objects.all() if p.user == request.user]

            for p in cart_products:
                tempamount = p.quantity * p.product.discounted_price
                amount += tempamount

            total_amount = amount + shipping_amount
            
            # Prepare the JSON response
            data = {
                'quantity': cart_item.quantity if cart_item.quantity > 0 else 0,
                'amount': amount,
                'totalamount': total_amount,
                'message': message,
            }

            return JsonResponse(data)

        except Cart.DoesNotExist:
            # Handle case where the cart item does not exist
            return JsonResponse({'error': 'Item not found in cart'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def remove_cart(request):
    if request.method=='GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        
        c.delete()
        amount=0.0
        shipping_amount=70.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user ==request.user]
        for p in cart_product:

            tempamount=(p.quantity * p.product.discounted_price)
            amount+=tempamount
        data={

            'amount': amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')
def auric(request):
    return render(request, 'app/auricbhoj.html')

 
@login_required
def address(request):
 add=Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/orders.html', {'order_placed':op})

 




# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
from django.core.mail import send_mail
from django.utils.html import format_html
from django.contrib.auth.models import User

from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import CustomerRegistrationForm
from .models import User, Customer
import random
from django.core.mail import send_mail
from django.http import HttpResponseForbidden

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            # Check if email is already taken
            if User.objects.filter(email=email).exists():
                messages.error(request, f"The email {email} is already associated with another account. Please use a different email.")
                return render(request, 'app/customerregistration.html', {'form': form})

            # Generate OTP
            otp = random.randint(100000, 999999)

            # Save the OTP and other details to the customer's session for later validation
            request.session['email'] = email
            request.session['otp'] = otp
            request.session['username'] = username

            # Create a new user but don't save yet
            user = User.objects.create_user(username=username, email=email, password=password)

            # Create the corresponding Customer object without saving it yet
            customer = Customer(user=user, Gmail=email)

            # Send OTP to the user's email
            subject = f"Your OTP for AuricMart Registration"
            html_message = f"""
            <html>
                <body>
                    <p>Your OTP for registering with AuricMart is <strong>{otp}</strong></p>
                    <p>Use this OTP to verify your account.</p>
                </body>
            </html>
            """
            try:
                send_mail(subject, '', 'niteshupa6@gmail.com', [email], html_message=html_message)
                messages.success(request, f"An OTP has been sent to {email}. Please verify.")
                return redirect('verify_otp')  # Redirect to OTP verification page
            except Exception as e:
                print(f"Email sending failed: {e}")
                messages.error(request, "Unable to send OTP email. Please contact support.")
                del request.session['email']
                del request.session['otp']
                del request.session['username']
                return redirect('customer_registration')

        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
            return render(request, 'app/customerregistration.html', {'form': form})

class OTPVerificationView(View):
    def get(self, request):
        # Display the OTP verification form
        return render(request, 'app/otp_verification.html')

    def post(self, request):
        otp = request.POST.get('otp')
        # Retrieve the OTP from the session
        session_otp = request.session.get('otp')

        if otp == str(session_otp):  # OTP is correct
            email = request.session.get('email')
            username = request.session.get('username')
            # Retrieve user using the email from the session
            user = User.objects.get(email=email)
            
            # Now save the user and customer object
            user.is_active = True  # Activate the user
            user.save()
            
            Customer.objects.create(user=user, Gmail=email)
            subject = f"Congratulations For AuricMart Registration"
            html_message = format_html(f"""
                <html>
                    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
                        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
                            <tr>
                                <td align="center" bgcolor="#004080" style="padding: 40px 0;">
                                    <h1 style="color: #ffffff; font-size: 24px;">Welcome, {username}!</h1>
                                </td>
                            </tr>
                            <tr>
                                <td bgcolor="#ffffff" style="padding: 20px 30px;">
                                    <p style="font-size: 18px; color: #333333;">
                                        Thank you Registered on AuricMart, the Best Divine Selling Partner! We’re thrilled to have you with us.
                                    </p>
                                    <p style="font-size: 16px; color: #333333;">
                                        We’re committed to making your experience as enjoyable as possible. If you have any questions, feel free to reach out!
                                    </p>
                                </td>
                            </tr>
                            <tr>
                                <td bgcolor="#004080" style="padding: 10px 30px; color: #ffffff; font-size: 14px; text-align: center;">
                                    <p>&copy; 2024 AuricMart. All rights reserved.</p>
                                    <p>123 Market Street, Ujajin, India</p>
                                    <p>Phone: +91-6260144580 | Email: auricmart37@gmail.com</p>
                                </td>
                            </tr>
                        </table>
                    </body>
                    </html>
                    """,
                    username=username)
            try:
                send_mail(subject, '', 'niteshupa6@gmail.com', [email], html_message=html_message)
                 # Redirect to OTP verification page
            except Exception as e:
                print(f"Email sending failed: {e}")
                messages.error(request, "Unable to send OTP email. Please contact support.")

            messages.success(request, "OTP verified successfully. Your account is now active.")
            return redirect('login')  # Redirect to login page after successful OTP verification

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, 'app/otp_verification.html')


class CustomerLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'app/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                # Retrieve email from Customer or fallback to User.email
                try:
                    customer = Customer.objects.get(user=user)
                    email = customer.Gmail
                except Customer.DoesNotExist:
                    email = user.email

                # Debugging email
                print(f"Email: {email}")

                # Construct and send the email
                subject = f"Congratulations {username}!"
                html_message = format_html(
                    """
                    <html>
                    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0;">
                        <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
                            <tr>
                                <td align="center" bgcolor="#004080" style="padding: 40px 0;">
                                    <h1 style="color: #ffffff; font-size: 24px;">Welcome, {username}!</h1>
                                </td>
                            </tr>
                            <tr>
                                <td bgcolor="#ffffff" style="padding: 20px 30px;">
                                    <p style="font-size: 18px; color: #333333;">
                                        Thank you for logging in on AuricMart, the Best Divine Selling Partner! We’re thrilled to have you with us.
                                    </p>
                                    <p style="font-size: 16px; color: #333333;">
                                        We’re committed to making your experience as enjoyable as possible. If you have any questions, feel free to reach out!
                                    </p>
                                </td>
                            </tr>
                            <tr>
                                <td bgcolor="#004080" style="padding: 10px 30px; color: #ffffff; font-size: 14px; text-align: center;">
                                    <p>&copy; 2024 AuricMart. All rights reserved.</p>
                                    <p>123 Market Street, Ujajin, India</p>
                                    <p>Phone: +91-6260144580 | Email: auricmart37@gmail.com</p>
                                </td>
                            </tr>
                        </table>
                    </body>
                    </html>
                    """,
                    username=username
                )

                send_mail(subject, '', 'niteshupa6@gmail.com', [email], html_message=html_message)

                # Check if the user belongs to the "Admin" group
                if user.groups.filter(name="Admin").exists():
                    return redirect('adminhome') 
                elif user.groups.filter(name="seller").exists():
                    return redirect('sellerhome') 
                 # Redirect admin users to admin home page
                else:
                    return redirect('home')  # Redirect non-admin users to the home page

            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

        return render(request, 'app/login.html', {'form': form})

def admin_group_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():  # Check if the user is in the 'admin' group
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
def seller_group_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.groups.filter(name='seller').exists():  # Check if the user is in the 'admin' group
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


import csv
@login_required
@admin_group_required
def admin_home(request):
    # Fetch data to display
    users = User.objects.all()
    products = Product.objects.all()
    orders = OrderPlaced.objects.all()
    customers = Customer.objects.all()

    context = {
        'users': users,
        'products': products,
        'orders': orders,
        'customers': customers,
    }
    return render(request, 'app/adminhome.html', context)


@login_required
@admin_group_required
def download_csv(request, model_name):
    # Determine model to export
    model_mapping = {
        'users': User,
        'products': Product,
        'orders': OrderPlaced,
        'customers': Customer,
    }

    if model_name not in model_mapping:
        return HttpResponse("Invalid model name", status=400)

    model = model_mapping[model_name]
    queryset = model.objects.all()

    # Create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_name}.csv"'
    writer = csv.writer(response)

    # Write header
    field_names = [field.name for field in model._meta.fields]
    writer.writerow(field_names)

    # Write data
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response


@login_required
@seller_group_required
def seller_home(request):
    # Filter products based on seller brand (e.g., 'seller1')
    seller_brand = "seller1"  # Adjust dynamically if seller's brand is linked to their user profile
    products = Product.objects.filter(brand=seller_brand)

    context = {
        'products': products,
        'seller_name': request.user.username,  # Display seller's name
    }
    return render(request, 'app/sellerhome.html', context)

@login_required
@seller_group_required
def download_csv1(request, model_name):
    if model_name != 'products':
        return HttpResponse("Invalid model for seller data export.", status=400)

    # Filter products only by the seller's brand
    seller_brand = "seller1"  # Adjust dynamically if linked to the user's profile
    queryset = Product.objects.filter(brand=seller_brand)

    # Create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    writer = csv.writer(response)

    # Write header
    field_names = [field.name for field in Product._meta.fields]
    writer.writerow(field_names)

    # Write data
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response

from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordResetForm

import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import make_password
  # Replace with the correct model

class CustomerPasswordResetView(View):
    def get(self, request):
        """
        Render the password reset form.
        """
        return render(request, 'app/resetpassword.html')

    def post(self, request):
        """
        Handle the password reset form submission.
        Generate and send a 6-digit OTP to the user's email.
        """
        username = request.POST.get('username')
        new_password = request.POST.get('password')

        try:
            # Fetch the customer with the provided email (username)
            customer = User.objects.get(email=username)

            # Generate a 6-digit OTP
            otp = random.randint(100000, 999999)

            # Save the OTP and other details to the customer's session for later validation
            request.session['reset_email'] = username
            request.session['password'] = new_password
            request.session['otp'] = otp

            # Send the OTP via email
            send_mail(
                subject="Your OTP for Password Reset",
                message=f"Your OTP for resetting your password is: {otp}",
                from_email="niteshupa6@gmail.com",  # Replace with your email
                recipient_list=[username],
                fail_silently=False,
            )

            # Redirect to the OTP validation page
            return redirect('otp_validation')

        except User.DoesNotExist:
            # If the email is not found, show an error and redirect to login page
            messages.error(request, "Email not found. Please try again.")
            return redirect('password_reset_ss')

        except Exception as e:
            # Handle any other unexpected errors
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('password_reset_ss')
        
class OTPValidationView(View):
    def get(self, request):
        """
        Render the OTP validation form.
        """
        return render(request, 'app/otpvalidation.html')

    def post(self, request):
        """
        Validate the OTP entered by the user.
        """

        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        reset_email = request.session.get('reset_email')
        password = request.session.get('password')

        if str(entered_otp) == str(session_otp):
            # OTP is valid; redirect to a page for entering the new password
            customer = User.objects.get(email=reset_email)
            customer.password = make_password(password)
            customer.save()
            messages.success(request, "You are successfully updated your password.")
            del request.session['otp']
            del request.session['reset_email']
            del request.session['password']
            return redirect('login')
            
        else:
            # OTP is invalid; re-render the OTP validation page with an error
            return render(
                request,
                'app/otpvalidation.html',
                {'error_message': 'Invalid OTP. Please try again.'}
            )

class CustomerLogoutView(View):
    def get(self, request):
        logout(request)  # Logs out the user
        messages.success(request, "You have successfully logged out.")
        return redirect('login')  # Redirect to login page or any other page

    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0

    # Get cart items for the current user
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]

    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.discounted_price
            amount += tempamount
        totalamount = amount + shipping_amount

    # Fetch the customer ID (assuming there's only one Customer instance per User)
    # You can adjust the query if there are multiple addresses or customers
    custid = add.first().id if add.exists() else None  # Get the first address/customer ID

    return render(request, 'app/checkout.html', {
        'add': add,
        'totalamount': totalamount,
        'cart_items': cart_items,
        'custid': custid  # Pass the customer ID to the template
    })



from django.utils.dateformat import DateFormat
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib.utils import ImageReader

from django.utils.dateformat import DateFormat
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from django.utils.dateformat import DateFormat
from django.http import HttpResponse
from app.models import OrderPlaced, Customer

def generate_invoice(request, order_id):
    # Fetch the order based on order_id
    order = OrderPlaced.objects.filter(id=order_id).first()
    customer = Customer.objects.filter(id=order.customer.id).first()  # Retrieve the customer by id

    # Debugging: Check if the order and customer are retrieved correctly
    if not order:
        print("Order not found")
        return HttpResponse("Order not found", status=404)
    if not customer:
        print("Customer not found")
        return HttpResponse("Customer not found", status=404)

    # Debugging: Check if the product details are available
    if not order.product:
        print("Product not found")
        return HttpResponse("Product not found", status=404)

    # Check if the customer and order data is correct
    print(f"Order ID: {order.id}")
    print(f"Order ID: {order.id}")
    print(f"Customer Name: {customer.name}")
    print(f"Product Title: {order.product.title}")

    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    # Create the PDF canvas
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Set the page background color (light orange example)
    p.setFillColor(colors.HexColor("#FFA500"))  # Light orange background
    p.rect(0, 0, width, height, fill=True)  # Fill the entire page with the background

    # Header Section
    header_height = 100
    p.setFillColor(colors.HexColor("#003366"))  # Dark blue background
    p.rect(0, height - header_height, width, header_height, fill=True)  # Adjust rectangle height

    # Title of the Invoice
    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(colors.white)
    p.drawString(200, height - header_height + 30, "AuricMart Invoice")

    # Customer Information Section
    customer_info_y = height - header_height - 50  # Position below header
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(40, customer_info_y, "Billing Address:")
    p.drawString(40, customer_info_y - 15, f"{customer.name}")
    p.drawString(40, customer_info_y - 30, f"{customer.city}, {customer.state}")
    p.drawString(40, customer_info_y - 45, f"Zipcode: {customer.zipcode}")
    p.drawString(40, customer_info_y - 60, f"Phone: {customer.mobile_number}")
    p.drawString(40, customer_info_y - 75, f"Email: {customer.Gmail}")


    # Right-aligned Information (Order ID, Customer Name, Product Title)
    right_margin = 250  # Margin from the right edge
    order_id_x = width - right_margin
    customer_name_x = width - right_margin
    product_title_x = width - right_margin

    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    
    # Print on the right side of the page
    p.drawString(order_id_x, customer_info_y, f"Order ID: {order.id}")
    p.drawString(customer_name_x, customer_info_y - 15, f"Customer Name: {customer.name}")
    p.drawString(product_title_x, customer_info_y - 30, f"Product Title: {order.product.title}")

    # Table Data for Products
    data = [
        ["Item", "Quantity", "Unit Price", "Amount"],
        [
            order.product.title,
            str(order.quantity),
            f"Rs. {order.product.selling_price:.2f}",
            f"Rs. {order.quantity * order.product.selling_price:.2f}"
        ]
    ]

    # Calculate totals
    subtotal = order.quantity * order.product.selling_price
    tax = subtotal * 0.18  # 18% tax
    delivery_fee = 70  # Fixed delivery fee
    grand_total = subtotal + delivery_fee + tax

    # Add totals to the table
    data.extend([
        ["", "", "", "", ""],  # Spacer row
        ["", "", "", "Subtotal", f"Rs. {subtotal:.2f}"],
        ["", "", "", "Tax (18%)", f"Rs. {tax:.2f}"],
        ["", "", "", "Delivery Charge", f"Rs. {delivery_fee:.2f}"],
        ["", "", "", "Grand Total", f"Rs. {grand_total:.2f}"]
    ])

    # Create and style the table
    table = Table(data, colWidths=[1.5 * inch, 2 * inch, 1 * inch, 1.25 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (2, -4), (-1, -1), 'RIGHT'),  # Align totals to the right
        ('FONTNAME', (2, -4), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (2, -4), (-1, -1), colors.black),
        ('SPAN', (0, -4), (2, -4)),  # Span spacer row
        ('SPAN', (0, -3), (2, -3)),  # Span empty cells in subtotal row
        ('SPAN', (0, -2), (2, -2)),  # Span empty cells in tax row
        ('SPAN', (0, -1), (2, -1)),  # Span empty cells in grand total row
    ]))

    # Draw table
    table.wrapOn(p, width - 100, height)
    table.drawOn(p, 40, customer_info_y - 220)  # Adjusted position

    # Add Company Address Section
    company_address_y = customer_info_y - 320
    p.setFont("Helvetica", 10)
    p.drawString(40, company_address_y, "Company Address:")
    p.drawString(40, company_address_y - 15, "AuricMart Pvt. Ltd.")
    p.drawString(40, company_address_y - 30, "123, Commerce Street, Business City")
    p.drawString(40, company_address_y - 45, "State, Zip: 123456")
    p.drawString(40, company_address_y - 60, "Phone: +91-9876543210")
    p.drawString(40, company_address_y - 75, "Email: support@auricmart.com")

    # Add Policy Section
    policy_y = company_address_y - 100
    p.setFont("Helvetica", 9)
    p.drawString(40, policy_y, "Return Policy:")
    p.drawString(40, policy_y - 15, "1. Items can be returned within 30 days of purchase.")
    p.drawString(40, policy_y - 30, "2. A valid receipt is required for all returns.")
    p.drawString(40, policy_y - 45, "3. Products must be in unused and original condition.")

    right_bottom_x = width - 300  # 200 points from the right edge
    right_bottom_y = 80  # 100 points from the bottom edge
    p.setFont("Helvetica", 9)

    # Adjusting y-values to avoid overlap
    p.drawString(right_bottom_x, right_bottom_y + 30, f"Order Date Time: {order.ordered_date}")
    p.drawString(right_bottom_x, right_bottom_y + 15, f"Order Status : {order.status}")
    p.drawString(right_bottom_x, right_bottom_y, f"Razorpay Order ID: {order.razorpay_order_id}")
    # Finalize and save the PDF
    p.showPage()
    p.save()

    return response

def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        user = request.user

        # Check if product is already in cart
        cart_item, created = Cart.objects.get_or_create(user=user, product=product)

        if not created:
            messages.info(request, f"{product.title} is already in your cart.")
        else:
            cart_item.quantity = 1
            cart_item.save()
            messages.success(request, f"Added {product.title} to your cart.")

    except Product.DoesNotExist:
        messages.error(request, "Product does not exist.")
    
    return redirect('showcart')

def update_cart_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))

        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)

            if quantity <= 0:
                cart_item.delete()  # Remove the item if quantity is 0
                return JsonResponse({'success': True, 'message': 'Item removed from cart'})
            else:
                cart_item.quantity = quantity
                cart_item.save()
                return JsonResponse({'success': True, 'message': 'Cart updated'})

        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found in cart'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        val = 0

        amount = sum(item.quantity * item.product.discounted_price for item in cart_items)

    # Increment val by 1 in each loop iteration
        for item in cart_items:
            val += 1  # Increase val by 1 for each loop iteration

        shipping_amount = 70 if amount > 0 else 0
        total_amount = amount + shipping_amount

        return render(request, 'app/addtocart.html', {
            'carts': cart_items,
            'amount': amount,
            'totalamount': total_amount,
            'val':val
        })
    else:
        return render(request, 'app/emptycart.html')
# Razorpay client initialization
import razorpay
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_API_SECRET))

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')

    if not custid:
        return HttpResponse("Customer ID is missing", status=400)

    try:
        # Fetch customer and cart data
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)

        if not cart:
            return HttpResponse("Cart is empty", status=400)

        # Calculate total amount (including shipping)
        total_amount = sum(c.quantity * c.product.discounted_price for c in cart) + 70  # Rs. 70 shipping charge

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": int(total_amount * 100),  # Convert amount to paise (integer value)
            "currency": "INR",
            "payment_capture": 1  # Automatic payment capture
        })

        # Save the order details in your database
        for c in cart:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=c.product,
                quantity=c.quantity,
                razorpay_order_id=razorpay_order['id']  # Save Razorpay order ID
            )
            # Delete cart item after placing the order
            c.delete()

        # Redirect to Razorpay payment page
        return render(request, 'app/razorpay_payment.html', {
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'total_amount': int(total_amount * 100),  # Convert to paise (integer value)
            'user': user,
        })

    except Customer.DoesNotExist:
        return HttpResponse("Customer not found", status=400)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

def cancel_order(request, order_id):
    """
    Cancel the order if it is not delivered.
    """
    order = get_object_or_404(OrderPlaced, id=order_id)
    
    # Check if the order is not delivered
    if order.status != 'Delivered':  # Replace 'status' and 'delivered' as per your model
        order.status = 'Cancel'  # Update the status
        order.save()
        messages.success(request, f"Order #{order_id} has been canceled.")
    else:
        messages.error(request, f"Order #{order_id} cannot be canceled as it is already delivered.")
    
    # Redirect back to the order page or any other page
    return redirect('orders')  # Replace 'order_page' with the actual name of the order page URL pattern

def verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    razorpay_secret = settings.RAZORPAY_API_SECRET
    string_to_hash = f"{razorpay_order_id}|{razorpay_payment_id}"
    generated_signature = hmac.new(
        bytes(razorpay_secret, 'utf-8'),
        bytes(string_to_hash, 'utf-8'),
        hashlib.sha256
    ).hexdigest()
    print(generated_signature)
    return generated_signature == razorpay_signature

import hmac
import hashlib
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import OrderPlaced, OrderItem
from django.contrib.auth.decorators import login_required

# Function to verify Razorpay signature
import hmac
import hashlib
from django.conf import settings

def verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    razorpay_secret = settings.RAZORPAY_API_SECRET

    # Create the string to hash: Razorpay order ID and payment ID
    string_to_hash = f"{razorpay_order_id}|{razorpay_payment_id}"
    
    # Generate the HMAC hash
    try:
        generated_signature = hmac.new(
            bytes(settings.RAZORPAY_API_SECRET, 'utf-8'),
            bytes(f"{razorpay_order_id}|{razorpay_payment_id}", 'utf-8'),
            hashlib.sha256
        ).hexdigest()
        print(f"Generated Razorpay Signature: {generated_signature}")
    except Exception as e:
        print(f"Error generating signature: {str(e)}")


    print(f"String to hash: {string_to_hash}")  # For debugging
    print(f"Generated signature: {generated_signature}")  # For debugging
    print(f"Received signature: {razorpay_signature}")  # For debugging

    return generated_signature == razorpay_signature

import hmac
import hashlib
from django.http import JsonResponse
from django.conf import settings
from .models import OrderPlaced, OrderItem
@login_required
def payment_verification(request):
    if request.method == "POST":
        try:
            # Retrieve Razorpay payment details from the POST request
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_signature = request.POST.get('razorpay_signature')

            # Check if all required parameters are available
            if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
                return JsonResponse({"status": "failure", "message": "Missing payment details"}, status=400)

            # Fetch the corresponding order from the database
            try:
                order = OrderPlaced.objects.get(razorpay_order_id=razorpay_order_id)
            except OrderPlaced.DoesNotExist:
                return JsonResponse({"status": "failure", "message": "Order not found"}, status=404)

            # Generate Razorpay signature using the Razorpay secret and order/payment IDs
            string_to_hash = f"{razorpay_order_id}|{razorpay_payment_id}"
            generated_signature = hmac.new(
                bytes(settings.RAZORPAY_API_SECRET, 'utf-8'),
                bytes(string_to_hash, 'utf-8'),
                hashlib.sha256
            ).hexdigest()

            # Debug print for generated signature (useful for troubleshooting)
            print(f"Generated Razorpay Signature: {generated_signature}")
            print(f"Received Razorpay Signature: {razorpay_signature}")

            # Verify if the generated signature matches the received signature
            if generated_signature == razorpay_signature:
                # Update order status to 'Accepted' upon successful payment verification
                order.status = 'Accepted'
                order.save()

                # Optionally send a confirmation email to the customer (you can implement email sending here)
                # send_confirmation_email(order)

                return JsonResponse({"status": "success", "message": "Payment verification successful, order confirmed"})

            else:
                return JsonResponse({"status": "failure", "message": "Invalid signature"}, status=400)

        except Exception as e:
            # Handle any unexpected errors gracefully
            return JsonResponse({"status": "failure", "message": f"An error occurred: {str(e)}"}, status=500)

    # Handle case where the request method is not POST
    return JsonResponse({"status": "failure", "message": "Invalid request method"}, status=405)
def home_view(request):
    # Define all categories dynamically
    categories = [
        {'name': 'Havan', 'url': 'havan', 'code': 'H'},
        {'name': 'Jadi', 'url': 'jadi', 'code': 'J'},
        {'name': 'Roodraksh', 'url': 'roodraksh', 'code': 'R'},
        {'name': 'Jap Mala', 'url': 'jap', 'code': 'JM'},
        {'name': 'Idols', 'url': 'idols', 'code': 'I'},
    ]
    
    # Prepare category data with products
    category_data = {}
    for category in categories:
        # Fetch products based on the category code
        products = Product.objects.filter(category=category['code'])  # Use 'category' instead of 'category_code'
        category_data[category['name']] = products  # Assign products to each category name

    return render(request, 'app/home.html', {'categories': categories, 'category_data': category_data})

def Havan(request):
    Havan_Samagri = Product.objects.filter(category='H').distinct()
    return render(request,'app/havan.html',{'Havan_Samagri': Havan_Samagri})

#         return render(request, 'app/havan.html', {'Spices': Spices})


def Jadi(request):
    jadi = Product.objects.filter(category='J').distinct()
    return render(request,'app/jadi.html',{'jadi': jadi}) 

def Roodraksh(request):
    Roodraksh = Product.objects.filter(category='R').distinct()
    
    return render(request,'app/roodraksh.html',{'Roodraksh': Roodraksh}) 

def Jap (request):
    jap = Product.objects.filter(category='JM').distinct()
    return render(request,'app/jap_mala.html',{'jap': jap}) 

def Idols (request):
    Idols = Product.objects.filter(category='I').distinct()
    
    return render(request,'app/idols.html',{'Idols':Idols}) 
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        # If the user already has a profile, prepopulate the form with existing data
        customer = Customer.objects.filter(user=request.user).first()
        form = CustomerProfileForm(instance=customer)
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        customer = Customer.objects.filter(user=request.user).first()
        if customer:
            # Update the existing customer instance
            form = CustomerProfileForm(request.POST, instance=customer)
        else:
            # Create a new customer instance
            form = CustomerProfileForm(request.POST)

        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user  # Ensure the user is linked
            customer.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully')
            return redirect('profile')  # Redirect to avoid duplicate form submissions

        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})