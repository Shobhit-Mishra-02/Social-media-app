from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _ 

from .managers import AccountUserManager

"""
Dummy users:
1. email: test@gmail.com, password: test123
2. email: raman@gmail.com, password: raman123
3. email: kevin@gmail.com, password: kevin123
"""

class AccountUser(AbstractUser):
    username = models.CharField(_("username"), blank=True, max_length=50)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountUserManager()

    def __str__(self) -> str:
        return self.email