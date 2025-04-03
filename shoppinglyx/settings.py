from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h=-gt1-a*phxr5_+gm0pm*__=_@_f&g%o30f^jpxo^1ipet#d-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'corsheaders',
    'chatbot',
    "storages",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

#CORS_ALLOWED_ORIGINS = [
    #'https://www.razorpay.com', # Razorpay origin

#]
CSRF_TRUSTED_ORIGINS = [
    'https://www.razorpay.com',
    'https://auricmart.com',
    'https://www.auricmart.com',
    'http://3.111.190.154',
]
CORS_ALLOWED_ORIGINS = [
    'https://auricmart.com',
    'https://www.auricmart.com',
    'http://3.111.190.154',
    'https://www.razorpay.com',
]
CORS_ALLOW_ALL_ORIGINS = False

ROOT_URLCONF = 'shoppinglyx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'chatbot/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shoppinglyx.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
# 'default': {
# 'ENGINE': 'django.db.backends.sqlite3',
# 'NAME': BASE_DIR / 'db.sqlite3',
# }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auricmar_d', # Your local MySQL database name
        'USER': 'auricmar_d', # Your local MySQL user
        'PASSWORD': 'vjHyKC3XKTaN', # Your local MySQL password
        'HOST': '148.113.14.27', # Localhost (or 'localhost')
        'PORT': '3306', # MySQL default port
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

#CSRF_TRUSTED_ORIGINS = [
    #'https://www.razorpay.com', # Razorpay origin
#]

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'auricmart37@gmail.com' # Your email address
EMAIL_HOST_PASSWORD = 'jxsy zilp rapa iqgh' # Use environment variable for security

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'app', 'static')
STATIC_URL = '/static/'

# Media files
#MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Login redirect URL
LOGIN_REDIRECT_URL = 'home'

# Razorpay configuration
RAZORPAY_KEY_ID = 'rzp_test_3cV94cjKhqlVA5'
RAZORPAY_API_SECRET = 'R4GSCdtIbU2EjtWpcXsPUgk6'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'error.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}


#AWS_ACCESS_KEY_ID = "0058c38d8fe75ed0000000001"
#AWS_SECRET_ACCESS_KEY = "K0052T6G9M6FhhhIZsYekmdKlO2daQ8"
#AWS_STORAGE_BUCKET_NAME = "auric123"
#AWS_S3_ENDPOINT_URL = "https://s3.us-east-005.backblazeb2.com" # Example: https://z2.idrivee2.com
#AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.us-east-005.backblazeb2.com"

AWS_ACCESS_KEY_ID = "005d7371227dcba0000000003"
AWS_SECRET_ACCESS_KEY = "K005fj2SVr1b3iqSmbDi8yL6W2PBqA4"
AWS_STORAGE_BUCKET_NAME = "auric1234"
AWS_S3_ENDPOINT_URL = "https://s3.us-east-005.backblazeb2.com" # Example: https://z2.idrivee2.com
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.us-east-005.backblazeb2.com"









AWS_S3_ADDRESSING_STYLE="virtual" # ✅ REQUIRED for Backblaze
AWS_QUERYSTRING_AUTH = False # Disable signed URLs for public access
AWS_DEFAULT_ACL = None # Avoid permission conflicts
# Static & Media Files Storage


# Static & Media Files Storage
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage" # For media files

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"



# Optional: Cache and file permissions
AWS_QUERYSTRING_AUTH = False # Public URLs