from django.core.mail import send_mail
import string
import random
from django.conf import settings
from django.urls import reverse

MY_HOST = settings.MY_HOST


def generate_link_account_detail(slug) -> dict:
    return f"{MY_HOST}{reverse(viewname='rest_account_detail', kwargs={'slug':slug})}"


def create_code() -> str:
    length = 6
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


def send_code(subject, message, email):
    from_email = settings.DEFAULT_FROM_EMAIL
    auth_password = settings.EMAIL_HOST_PASSWORD
    auth_user = settings.EMAIL_HOST_USER
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        auth_password=auth_password,
        auth_user=auth_user,
        recipient_list=[email],
    )
