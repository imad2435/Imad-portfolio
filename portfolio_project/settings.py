# imad/portfolio_project/settings.py

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE SETTINGS ---
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-a-strong-default-key-for-dev')
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', os.getenv('VERCEL_URL')]

# --- APPLICATION DEFINITION ---
# We add 'django_htmx' to our installed apps.
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'django_htmx',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware', # Add HTMX middleware
]

ROOT_URLCONF = 'portfolio_project.urls'

# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'portfolio_project.wsgi.application'

# --- DATABASE & PASSWORD VALIDATION ---
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC & MEDIA FILES ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# --- DJANGO DEFAULTS ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- AUTHENTICATION AND REDIRECT SETTINGS ---
# After a user logs in, redirect them to our custom dashboard.
LOGIN_REDIRECT_URL = '/dashboard/'
# If a user tries to access a page that requires login, send them here.
LOGIN_URL = '/dashboard/login/'