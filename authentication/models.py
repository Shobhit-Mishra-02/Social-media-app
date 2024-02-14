from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import AccountUserManager

"""
This the class of our custom user model, where email attribute is used as the primary key. 

The default user model class contains username attribute which is used for primary key, in order to change it a new user class is created. 
"""


class AccountUser(AbstractUser):
    username = models.CharField(_("username"), blank=True, max_length=50)
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountUserManager()

    def __str__(self) -> str:
        return self.email
