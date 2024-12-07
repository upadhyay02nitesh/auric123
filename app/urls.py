from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MySetPasswordForm
from .views import OTPVerificationView, ProductDetailView, submit_review,CustomerLoginView,CustomerPasswordResetView,OTPValidationView
urlpatterns = [

    # path('', views.home),
    
    path('search/', views.search_view, name='search'),
    path('book_schedule/', views.book_schedule, name='book_schedule'),
    path('my_bookings/', views.my_bookings, name='bookings'),

    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:product_id>/reviews/', views.get_reviews, name='get_reviews'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('auric/', views.auric, name='auric'),
    path('about/', views.about, name='about'),
    path('pandit/', views.pandit, name='pandit'),
     path('add_pandit/', views.add_pandit, name='add_pandit'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('adminhome/', views.admin_home, name='adminhome'),
    path('sellerhome/', views.seller_home, name='sellerhome'),
    path('download_csv/<str:model_name>/', views.download_csv, name='download_csv'),
    path('download_csv1/<str:model_name>/', views.download_csv1, name='download_csv1'),
    path('verify_otp/', OTPVerificationView.as_view(), name='verify_otp'),
    path('password_reset_ss/', CustomerPasswordResetView.as_view(), name='password_reset_ss'),
    path('otp_validation/', OTPValidationView.as_view(), name='otp_validation'),
    path('submit-review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('', views.home_view, name='home'),
     path('Havan/', views.Havan, name='havan'),
    path('Jadi/', views.Jadi, name='jadi'),
    path('Roodraksh/', views.Roodraksh, name='roodraksh'),
    path('Jap/', views.Jap, name='jap'),
    path('Idols/', views.Idols, name='idols'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),


    path('address/', views.address, name='address'),
     path('paymentdone/', views.payment_done, name='payment_done'),
    path('payment-verification/', views.payment_verification, name='payment_verification'),
    path('orders/', views.orders, name='orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
   
    path('generate_invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),

    path('payment/', views.checkout, name='payment'),
    path('paymentdone/', views.payment_done, name='paymentdone'),


    # path('login/', views.login, name='login'),
    path('accounts/login/', CustomerLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'),name='logout'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',
    form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'),
    name='passwordchange'),


    path('passwordchangedone/', auth_views.PasswordChangeDoneView.
    as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),



    path('checkout/', views.checkout, name='checkout'),
    path('registration/',views.CustomerRegistrationView.as_view(), name="customerregistration")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),