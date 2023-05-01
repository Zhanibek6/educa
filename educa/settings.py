"""
Django settings for educa project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from django.urls import reverse_lazy
from environs import Env
from google.oauth2 import service_account

env = Env()
env.read_env()  # read .env file, if it exists


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production! Removed for differentiate environments
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "educa-project.fly.dev"]


# Application definition
INSTALLED_APPS = [
    "daphne",  # Caution with whitenoise (daphne must at the top)
    # My apps
    "courses.apps.CoursesConfig",
    "accounts.apps.AccountsConfig",
    "pages.apps.PagesConfig",
    "chat",
    "quizes.apps.QuizesConfig",
    "grappelli",  #  A jazzy skin for the admin. 3rd party for filebrowser
    "filebrowser",  # Uploads files in tinyMCE
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # whitenoise 3rd-party
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third party
    "embed_video",  # TEMPLATE_CONTEXT_PROCESSORS HTTP/S!
    "django_quill",  # editor like tinymce
    "debug_toolbar",
    "redisboard",
    "rest_framework",
    "tinymce",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_cleanup.apps.CleanupConfig",  # auto-delete
    "django_extensions",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "educa.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "educa.wsgi.application"


# Database (Removed for differentiate environments)
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {"default": env.dj_db_url("DATABASE_URL", default="sqlite:///db.sqlite3")}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ru-RU"

USE_I18N = True

# TimeZone
USE_TZ = True
TIME_ZONE = "Asia/Almaty"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Settings for media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# django-storages[google]
# GOOGLE_APPLICATION_CREDENTIALS = BASE_DIR / "educa-django-storages-c3e9cf3e3b0f.json"
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    "educa-django-storages_keys.json"
)
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = "bucket-django-educa"
GS_FILE_OVERWRITE = False  # Не перезаписывать файлы с одинаковыми именами
# GS_MAX_MEMORY_SIZE = 1000000  # Макс объем файла в байтах


# Settinf for django-filebrowser (выключил)
FILEBROWSER_DIRECTORY = ""
DIRECTORY = ""
TINYMCE_FILEBROWSER = True  # Не включать в tinyMCE
# X_FRAME_OPTIONS = "SAMEORIGIN"  # Чтобы filebrowser работал в tinyMCE

# redis
CACHES = {"default": env.dj_cache_url("REDIS_URL")}

CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 15 * 60
CACHE_MIDDLEWARE_KEY_PREFIX = "educa"

# debug-toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# Rest API
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ]
}

# TinyMCE

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 500,
    "cleanup_on_startup": True,
    "custom_undo_redo_levels": 20,
    "selector": "textarea",
    "theme": "silver",
    "plugins": """
            textcolor save link preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak spellchecker
            """,
    "toolbar1": """
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            """,
    "toolbar2": """
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            """,
    "contextmenu": "formats | link image",
    "menubar": True,
    "statusbar": True,
    "images_upload_url": "upload_image",
}
# TINYMCE_SPELLCHECKER = True

QUILL_CONFIGS = {
    "default": {
        "theme": "snow",
        "modules": {
            "syntax": True,
            "toolbar": [
                [
                    {"font": []},
                    {"header": []},
                    {"align": []},
                    "bold",
                    "italic",
                    "underline",
                    "strike",
                    "blockquote",
                    {"color": []},
                    {"background": []},
                ],
                ["code-block", "link"],
                ["clean"],
            ],
        },
    }
}

# django-crispy-forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# django-allauth
AUTH_USER_MODEL = "accounts.CustomUser"  # Custom User

LOGIN_REDIRECT_URL = reverse_lazy("student_course_list")
LOGOUT_REDIRECT_URL = "course_list"

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SESSION_REMEMBER = True

SITE_ID = 1

ACCOUNT_FORMS = {
    "signup": "accounts.forms.CustomSignupForm",
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # django backend
    "allauth.account.auth_backends.AuthenticationBackend",  # allauth backend
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"




# ASGI
ASGI_APPLICATION = "educa.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": env.list("REDIS_URL"),  #
        },
    },
}

# for production
# A list of trusted origins for "unsafe" request that use POST
CSRF_TRUSTED_ORIGINS = ["https://educa-project.fly.dev"]

# Add compression and caching support by whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Security
SECURE_SSL_REDIRECT = env.bool(
    "DJANGO_SECURE_SSL_REDIRECT", default=True
)  # HTTP requests redirected to HTTPS
# Отказывать в подключение в течении времени через незащищенное соединение (пока что час, нужно больше)
SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=3600)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)  # subdomains via https
SECURE_HSTS_PRELOAD = env.bool(
    "DJANGO_SECURE_HSTS_PRELOAD", default=True
)  # submit for inclusion preload

SESSION_COOKIE_SECURE = env.bool(
    "DJANGO_SESSION_COOKIE_SECURE", default=True
)  # The cookie over only HTTPS
CSRF_COOKIE_SECURE = env.bool(
    "DJANGO_SESSION_COOKIE_SECURE", default=True
)  # only cookies marked as "secure"

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)  # Найти правильный заголовок прокси fly
