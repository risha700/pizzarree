"""
Django settings for pizzarree_api project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import secrets
import sys
from ast import literal_eval
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PROJECT_NAME = os.getenv('DJANGO_PROJECT_NAME', 'Pizzarree Shop')
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TESTING = sys.argv[1:2] == ['test']
FRONTEND_URL = os.getenv('DJANGO_FRONTEND_URL', 'https://pizzarree.net')
API_WEBHOOK_REDIRECT_EXTENSION = os.getenv('DJANGO_API_WEBHOOK_REDIRECT_EXTENSION', 'done')
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', secrets.token_urlsafe(38))
# GEOIP_PATH = os.getenv('DJANGO_GEOIP_PATH', os.path.join(BASE_DIR, '../GeoLite'))
DEBUG = bool(literal_eval(os.getenv('DJANGO_DEBUG', '1')))
ADMIN_SITE_PATH = os.getenv('DJANGO_ADMIN_SITE_PATH', 'admin')
SUPPORT_MAIL = "support@pizzarree.net"


AUTH_USER_MODEL = "accounts.User"
DEFAULT_FROM_EMAIL = "info@pizzarree.test"
ALLOWED_HOSTS = ["*"]

# EMAIL_BACKEND = "django.core.mail.backendnds.console.EmailBackend"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = 'a571812ba39b6d'
EMAIL_HOST_PASSWORD = 'ee0e4489a103b8'
EMAIL_PORT = '2525'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'accounts',
    'shop',
    'django_phonenumbers',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pizzarree_api.urls'
STATIC_URL = '/static/' #alias for static_root
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_src")
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'pizzarree_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'accounts.authentication.EmailAuthBackend',
    'accounts.authentication.PhoneAuthBackend',
    'accounts.authentication.UsernameAuthBackend'
]
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'common',
    'access-control-allow-origin',
    'access-control-allow-credentials',

)
# CORS_ALLOWED_ORIGINS = os.environ.get('DJANGO_CORS_ALLOWED_ORIGINS', "http://localhost:8080").split(',')
# CORS_ALLOWED_ORIGIN_REGEXES = [fr"{os.environ.get('DJANGO_CORS_ALLOWED_ORIGIN_REGEXES', None)}"]
CSRF_TRUSTED_ORIGINS =os.environ.get('DJANGO_CORS_ALLOWED_ORIGINS', "http://localhost:8080").split(',')
CORS_ALLOW_CREDENTIALS = True
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES' : ('rest_framework.renderers.JSONRenderer',),
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.DjangoModelPermissions',
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    # 'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
    # 'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
CART_SESSION_ID = 'cart'

STRIPE_API_KEY = os.getenv('DJANGO_STRIPE_API_KEY', 'pk_test_RUZqAN8CkTK39VGr7FuIxPWE')
STRIPE_API_SECRET = os.getenv('DJANGO_STRIPE_API_KEY', 'sk_test_CHbkFTgQWREZlA5ff17sCy1Q')


