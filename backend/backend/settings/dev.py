from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test-db.sqlite3",
    }
}


BASE_INVOICE_TEMPLATE = BASE_DIR / "drscm/templates/word/style.docx"

# LOGGING = {
#     "version": 1,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#     },
#     "loggers": {
#         "django.db.backends": {
#             "level": "DEBUG",
#         },
#     },
#     "root": {
#         "handlers": ["console"],
#     },
# }
