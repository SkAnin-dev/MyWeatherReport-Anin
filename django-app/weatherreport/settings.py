# You should not edit this file
from django.contrib import messages
from pathlib import Path
import tempfile

BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings for development; can update for production as needed.
DEBUG = False
ALLOWED_HOSTS = ['http://localhost:3000/']
CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
ALLOWED_HOSTS = ['127.0.0.1', 'localhost',  'aninsweatherapp-f5b283b0070f.herokuapp.com']


SECRET_KEY = 'django-insecure-session-key'

# For our React SPA, explicitly allow unauthenticated users.
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    # Optional: if you wish to use data_wizard for development,
    'data_wizard',
    'data_wizard.sources',
    # Optional: if using crispy forms
    'crispy_forms',
    'crispy_bootstrap5',
    #'weather',        # weather app
    'weather.apps.WeatherConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# Update the root URL configuration to use your project module.
ROOT_URLCONF = 'weatherreport.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add custom template directories here if needed.
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

# WSGI application configuration.
WSGI_APPLICATION = 'weatherreport.wsgi.application'

# Database for development (SQLite).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalisation settings.
LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [('en', 'English')]

# Locale path updated for the weather app.
LOCALE_PATHS = [BASE_DIR / 'weather' / 'locale']

# Static files settings.
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'react-app' / 'build',  # if you're including a React build
]

# Media files settings.
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

# Optional: Configuration for crispy forms if used.
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Account redirect URLs.
#LOGOUT_REDIRECT_URL = '/'
#LOGIN_REDIRECT_URL = '/'

# Use the default Django user model (custom user model removed).
# AUTH_USER_MODEL = 'label_music_manager.MusicManagerUser'  # Removed

# Remove duplicate REST_FRAMEWORK block.

CORS_ALLOW_ALL_ORIGINS = True

# Email Backend: saves emails to a temporary directory for development.
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
DEFAULT_FROM_EMAIL = 'sa03742@surrey.ac.uk'
EMAIL_FILE_PATH = tempfile.mkdtemp()

