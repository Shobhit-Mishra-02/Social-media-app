from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

"""
Creating Manager class for our custom user model, which actually includes methods like create_user and create_superuser
"""


class AccountUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        # checking for the presence of email
        if not email:
            raise ValueError(_("The Email must be set"))

        # checking for the presence of password
        if not password:
            raise ValueError(_("The password must be set"))

        email = self.normalize_email(email)  # lowercasing any capital alpabet

        # asigning email to the user model
        user = self.model(email=email, **extra_fields)

        # setting the user password
        user.set_password(password)

        # then, saving the user
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        # setting the fields in a such a way which gives all powers to the super user
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # the is_staff attribute should always be True for a super user
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))

        # the is_stuperuser attribute should always be True for a super user
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create_user(email, password, **extra_fields)
