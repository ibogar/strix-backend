from .base import *

SECRET_KEY = "django-insecure-px6il9(a=j3)qqkqdfpbi21kmpgf)fc0g24k&!aku9h77sf&oq"

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]