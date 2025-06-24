# imad/portfolio_project/settings.py

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CORE SECURITY & HOSTING SETTINGS
# ==============================================================================

# Get the secret key from an environment variable. Use a default for local development.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-a-default-secret-key-for-local-dev-only')

# DEBUG is False in production on Render, True for local development.
# The 'RENDER' environment variable is automatically set by Render.
DEBUG = 'RENDER' not in os.environ

# Configure allowed hosts.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Add the Render external hostname to ALLOWED_HOSTS if it exists.
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

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
    # WhiteNoise must be placed directly after the security middleware.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'portfolio_project.urls'


# ==============================================================================
# TEMPLATES
# ==============================================================================

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


# ==============================================================================
# DATABASE
# ==============================================================================

if DEBUG:
    # Local development database (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Production database on Render (PostgreSQL)
    # The DATABASE_URL is provided by Render's environment.
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            ssl_require=True
        )
    }


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

# --- STATIC FILES (CSS, JS) ---
STATIC_URL = '/static/'
# This is where 'collectstatic' will gather all static files.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Tell WhiteNoise to serve files from this directory.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- MEDIA FILES (User Uploads) ---
MEDIA_URL = '/media/'
# Use a different root for production vs. local development.
if DEBUG:
    # Local: Store media in a 'mediafiles' folder in your project root.
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
else:
    # Production (Render): Store media on the persistent disk.
    # This path MUST match the "Mount Path" for the Disk on Render.
    MEDIA_ROOT = '/var/data/media'


# ==============================================================================
# DJANGO DEFAULTS
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# AUTHENTICATION AND REDIRECT SETTINGS
# ==============================================================================

LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/dashboard/login/'