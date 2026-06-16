from .base import *

import os
import dj_database_url

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = [
    ".railway.app",
]

DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
    )
}

CORS_ALLOWED_ORIGINS = [
    "https://strix-cyan.vercel.app",
]