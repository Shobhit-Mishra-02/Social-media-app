from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _ 

from .managers import AccountUserManager

class AccountUser(AbstractUser):
    username = models.CharField(_("username"), blank=True, max_length=50)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountUserManager()

    def __str__(self) -> str:
        return self.email