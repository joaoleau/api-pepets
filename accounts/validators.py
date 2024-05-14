from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def name_validator(name: str):
    if len(name) < 3:
        raise ValidationError(_("Name must be at least 4 characters long"))
    return name


def password_validator(password):
    if not re.search(r"[A-Z]", password):
        raise ValidationError(
            _("The password must contain at least one uppercase letter")
        )

    if not re.search(r"[a-z]", password):
        raise ValidationError(
            _("The password must contain at least one lowercase letter")
        )

    if not re.search(r"\d", password):
        raise ValidationError(_("The password must contain at least one digit"))

    if not re.search(r"[!@#$%^&*(),.?:{}|<>]", password):
        raise ValidationError(_("The password must contain special characters"))

    if len(password) < 6:
        raise ValidationError(_("The password must be at least 6 characters long"))

    return password
