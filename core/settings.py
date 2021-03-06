"""
Django settings for remzona project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-r&nb2s$1ic(o11vc(1e^zhwloccibl!%k0)v1v(xxag4@7@h3="
)

# TODO SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]  # TODO
AUTH_USER_MODEL = "rest_auth.User"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Rest implementation for Django framework.
    "rest_framework",
    "rest_framework.authtoken",
    # Generate Swagger/OpenAPI 3.0 specifications from a Django Rest Framework API.
    # Documentation: https://drf-spectacular.readthedocs.io/
    "drf_spectacular",
    # Integrated set of Django applications addressing authentication,
    # registration, account management as well as 3rd party (social) account authentication.
    "allauth",
    "allauth.account",
    # Rest auth provider for allauth
    "dj_rest_auth",
    # A Django App that adds Cross-Origin Resource Sharing (CORS) headers to responses.
    # This allows in-browser requests to your Django application from other origins.
    # Documentation: https://pypi.org/project/django-cors-headers/
    "corsheaders",
    # Custom apps
    "api",
    "rest_auth",
    "api.apps.work_process",
    "api.apps.analytics",
    "api.apps.cars",
    "api.apps.bonuses",
    # "api.apps.advertising",
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    # Needed to login by username in Django admin, regardless of `allauth`
    "allauth.account.auth_backends.AuthenticationBackend",
)


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "core.urls"


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


WSGI_APPLICATION = "core.wsgi.application"


# CORS SETTINGS

CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = ()
# CORS_ALLOW_CREDENTIALS = True # ?????????????????? ?????????????????????????? ?????????? ?????? ??????????-???????????????? ????????????????

# REST FRAMEWORK SETTINGS

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "core.exceptions.exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    # "DATETIME_INPUT_FORMATS": [
    #     "%Y-%m-%d %H:%M",
    # ],
    # "DATETIME_FORMAT": "%Y-%m-%d %H:%M",
}

# DJ_REST_AUTH SETTINGS

REST_USE_JWT = True
JWT_AUTH_COOKIE = "remzona-access"
JWT_AUTH_REFRESH_COOKIE = "remzona-refresh"

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "rest_auth.serializers.UserDetailsSerializer"
}


# SIMPLE_JWT SETTINGS
if DEBUG:
    access_token_lifetime = timedelta(days=5)
else:
    access_token_lifetime = timedelta(minutes=15)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": access_token_lifetime,
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
}


# DRF_SPECTACULAR SETTINGS

SPECTACULAR_SETTINGS = {
    "TITLE": "Remzona-CRM API",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,  # hide schema endpoint
    "SWAGGER_UI_SETTINGS": {
        "defaultModelsExpandDepth": -1,
        "filter": True,
    },
    "DISABLE_ERRORS_AND_WARNINGS": True,
    "COMPONENT_SPLIT_REQUEST": True,
    "SORT_OPERATIONS": False,
}


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "PORT": os.getenv("POSTGRES_PORT", 5432),
        "ATOMIC_REQUESTS": True,  # ???????????? ???? ??????????????????????
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

if not DEBUG:
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
            "OPTIONS": {"min_length": 7},
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# if DEBUG:
#     MEDIA_URL = '/media/'
#     STATICFILES_DIRS = [
#         os.path.join(BASE_DIR, 'static')
#     ]
#     MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CUSTOM PARAMETERS

API_VERSION = os.getenv("API_VERSION", "v1.0")
API_URL = "api/%s/" % API_VERSION
MODERATOR_GROUP_NAME = os.getenv("MODERATOR_GROUP_NAME", "master-receiver")
REGULAR_USERS_GROUP_NAME = os.getenv("REGULAR_USERS_GROUP_NAME", "master-regular")

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
