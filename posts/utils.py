from django.urls import reverse
from django.conf import settings


def generate_link_post_detail(slug) -> dict:
    return f"{settings.MY_HOST}{reverse(viewname='posts:rest_post_detail', kwargs={'slug':slug})}"
