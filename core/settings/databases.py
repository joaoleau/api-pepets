from decouple import config

ENGINE_DB = config("DATABASE_ENGINE", default="django.db.backends.sqlite3")
NAME_DB = config("DATABASE_NAME", default="")
USER_DB = config("DATABASE_USER", default="")
PASSWORD_DB = config("DATABASE_PASSWORD", default="")
HOST_DB = config("DATABASE_HOST", default="")
PORT_DB = config("DATABASE_PORTB", default="")

DATABASES = {
    "default": {
        "ENGINE": ENGINE_DB,
        "NAME": NAME_DB,
        "USER": USER_DB,
        "PASSWORD": PASSWORD_DB,
        "HOST": HOST_DB,
        "PORT": PORT_DB,
    }
}
