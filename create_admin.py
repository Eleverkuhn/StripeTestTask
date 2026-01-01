import os

import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "payments.settings")

django.setup()

from config import settings


def create_superuser() -> None:
    user = get_user_model()
    if not user.objces.filter(username=settings.admin_username).exists():
        user.objects.create_superuser(username=settings.admin_username,
                                      email=settings.admin_email,
                                      password=settings.admin_password)
