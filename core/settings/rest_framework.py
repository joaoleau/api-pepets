from datetime import timedelta
from decouple import config

LOGIN_URL = "login/"
LOGIN_REDIRECT_URL = "posts/"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.BasicAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "BLACKLIST_AFTER_ROTATION": True,
    "ROTATE_REFRESH_TOKENS": True,
    "SIGNING_KEY": config("SECRET_KEY_JWT", "INSECURE"),
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Pepets API",
    "DESCRIPTION": "Backend com Django Rest - APIRestful. Projeto consiste em um site de achados e perdidos de pets",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
