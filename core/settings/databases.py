from decouple import config

NAME_DB = config("NAME_DB", default="")
USER_DB = config("USER_DB", default="")
PASSWORD_DB = config("PASSWORD_DB", default="")
HOST_DB = config("HOST_DB", default="")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": NAME_DB,
        "USER": USER_DB,
        "PASSWORD": PASSWORD_DB,
        "HOST": HOST_DB,
        "PORT": "5432",
    }
}
