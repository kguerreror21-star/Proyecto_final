
import os
from pathlib import Path
import dj_database_url

# ==============================
# BASE
# ==============================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# SEGURIDAD
# ==============================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-adventurero-change-me"
)

DEBUG = False

ALLOWED_HOSTS = ["*"]

# ==============================
# APLICACIONES
# ==============================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "core",
]

# ==============================
# MIDDLEWARE
# ==============================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise para archivos estáticos
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==============================
# URLS
# ==============================

ROOT_URLCONF = "adventurero.urls"

# ==============================
# TEMPLATES
# ==============================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==============================
# WSGI
# ==============================

WSGI_APPLICATION = "adventurero.wsgi.application"

# ==============================
# BASE DE DATOS
# ==============================


if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.parse(
            os.environ.get("DATABASE_URL")
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }



# ==============================
# VALIDADORES PASSWORD
# ==============================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

# ==============================
# INTERNACIONALIZACIÓN
# ==============================

LANGUAGE_CODE = "es-co"

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_TZ = True

# ==============================
# ARCHIVOS ESTÁTICOS
# ==============================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    ("css", BASE_DIR / "css"),
    ("js", BASE_DIR / "js"),
    ("img", BASE_DIR / "img"),
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# ==============================
# MEDIA
# ==============================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"

# ==============================
# LOGIN / LOGOUT
# ==============================

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "home"

LOGOUT_REDIRECT_URL = "home"

# ==============================
# DEFAULT AUTO FIELD
# ==============================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

