from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, **extra_fields):
        if not email:
            raise ValueError("You must provide an email address")

        first_name = first_name.capitalize()
        last_name = last_name.capitalize()
        email = self.normalize_email(email)

        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(first_name, last_name, email, password, **extra_fields)

    def create_adminuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(first_name, last_name, email, password, **extra_fields)
