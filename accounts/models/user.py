from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
import string
import random
import uuid


class User(AbstractUser):

    slug = models.SlugField(
        verbose_name=_("A short label for URLs"),
        max_length=100,
        unique=True,
        blank=True,
        null=True,
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,12}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 12 digits allowed.",
    )
    phone = models.CharField(
        validators=[phone_regex], max_length=20, unique=True, blank=True, null=True
    )
    email = models.EmailField(_("email address"), max_length=100, unique=True)
    first_name = models.CharField(_("first name"), max_length=100, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    _code = models.UUIDField(editable=False, default=None)
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "first_name", "last_name"]

    def save(self, *args, **kwargs):
        if not self._code:
            self.code = uuid.uuid4()
        if not self.slug:
            self.slug = slugify(
                f'{self.first_name}{"".join(random.choice(string.digits) for _ in range(4))}'
            )
        return super(User, self).save(*args, **kwargs)

    def email_user(self, subject, **kwargs):
        viewname = kwargs.pop("viewname")
        url = (
            f"{settings.MY_HOST}{reverse(viewname=viewname, kwargs={'uuid':self.code})}"
        )
        send_mail(
            subject=subject, message=url, recipient_list=[self.email], from_email=None
        )

    @property
    def code(self):
        self._code = uuid.uuid4()
        self.save()
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-date_joined",)
