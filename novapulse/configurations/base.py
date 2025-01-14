"""
Django settings for novapulse project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-6cf38&s=gt$at2v4j_h4=qau1dscp1j+0+j3h!*@e43f0p&t2&"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.arbitrage_scanner",
    "channels"
]

MIDDLEWARE = [
    "log_request_id.middleware.RequestIDMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "novapulse.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "novapulse.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": os.environ.get("NOVAPULSE_DB"),
        "USER": os.environ.get("NOVAPULSE_DB_USER"),
        "PASSWORD": os.environ.get("NOVAPULSE_PASSWORD"),
        "HOST": os.environ.get("NOVAPULSE_DB_HOST"),
        "PORT": os.environ.get("NOVAPULSE_DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter',
        },
    },
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(request_id)s] [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'verbose',
        },
        'application': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'backupCount': 3,
            'filename': 'logs/novapulse.log',
            'formatter': 'verbose',
            'filters': ['request_id'],
        },
        'worker': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'backupCount': 3,
            'filename': 'logs/worker.log',
            'formatter': 'verbose',
            'filters': ['request_id'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'application'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'application'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console', 'application'],
        },
        'celery': {
            'handlers': ['worker', 'console'],
            'level': 'INFO',
        },
        'apps': {
            'handlers': ['console', 'application'],
            'level': 'INFO',
        },
        'root': {
            'handlers': ['console', 'application'],
            'level': 'INFO',
        },
    },
}

BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY', '')
BINANCE_SECRET = os.environ.get('BINANCE_SECRET', '')
BITQUERY_API_URL = os.environ.get('BITQUERY_API_URL', '')
BITQUERY_AUTH_TOKEN = os.environ.get('BITQUERY_AUTH_TOKEN', '')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

