from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# django-environ
env = environ.Env()

try:
    environ.Env.read_env(env_file=".env")
except FileNotFoundError:
    pass


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

SECRET_KEY = env("DJANGO_SECRET_KEY", default="django-insecure-+%2m6r#4#=@i=)=f#mo_7)ye&c5ub+1&_l^+u8^a$s(j+-&(")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.Account"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
]


# ==============================================================================
# APPS SETTINGS
# ==============================================================================

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    # djangorestframework
    "rest_framework",
    # django-imagekit
    "imagekit",
]

LOCAL_APPS = [
    "apps.core.apps.CoreConfig",
    "apps.accounts.apps.AccountsConfig",
    "apps.plans.apps.PlansConfig",
    "apps.images.apps.ImagesConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================

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


# ==============================================================================
# AUTHENTICATION AND AUTHORIZATION SETTINGS
# ==============================================================================

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

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]


# ==============================================================================
# INTERNATIONALIZATION SETTINGS
# ==============================================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"


# ==============================================================================
# MEDIA FILES SETTINGS
# ==============================================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# XXX, NOTE: Custom settings for the purpose of generating thumbnails links
# in apps.images.api.serializer.ImageSerializer.to_representation() override.
# This should be reviewed when the domaign changes (for example to AWS S3 or other third party).
DEFAULT_MEDIA_DOMAIN = env("DEFAULT_MEDIA_DOMAIN", default="http://127.0.0.1:8000")


# ==============================================================================
# THIRD-PARTY SETTINGS
# ==============================================================================

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAdminUser",),
}

# Django Sesame

AUTHENTICATION_BACKENDS += [
    "sesame.backends.ModelBackend",
]

SESAME_MAX_AGE = 300  # arbitrary value, it can be updated on a per view basis
