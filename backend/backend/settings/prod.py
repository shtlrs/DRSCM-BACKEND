from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
