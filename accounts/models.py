from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils.text import slugify
from .utils import create_code
import string
import random


class User(AbstractUser):

    class RoleOptions(models.TextChoices):
        ADMIN = (
            "admin",
            "Admin",
        )
        STAFF = (
            "staff",
            "Staff",
        )
        CUSTOMER = "customer", "Customer"

    slug = models.SlugField(
        verbose_name="A short label for URLs", max_length=100, blank=True, null=True
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,12}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.",
    )
    phone = models.CharField(
        validators=[phone_regex], max_length=20, unique=True, blank=True, null=True
    )
    email = models.EmailField(_("email address"), max_length=100, unique=True)
    role = models.CharField(max_length=100, default=RoleOptions.CUSTOMER)
    first_name = models.CharField(_("first name"), max_length=100, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    email_validated = models.BooleanField(default=False)
    bio = models.TextField(max_length=200, blank=True)
    username = None
    code = models.CharField(max_length=6, default=create_code())

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "first_name", "last_name"]

    def save(self, *args, **kwargs):
        self.slug = slugify(
            f'{self.first_name}{"".join(random.choice(string.digits) for _ in range(4))}'
        )
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-date_joined",)
