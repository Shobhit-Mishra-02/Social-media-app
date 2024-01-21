from django.db import models
from django.utils import timezone
from authentication.models import AccountUser
from django.utils.translation import gettext_lazy as _
from home.utils.get_countries import get_country_names


COUNTRY_NAMES = get_country_names()
GENDERS = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]


class Post(models.Model):
    user = models.ForeignKey(
        AccountUser, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(_("Title of post"), max_length=200, blank=False)
    content = models.TextField(_("Content of of post"), blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    image = models.ImageField(
        _("Image for post"), upload_to="images", blank=True)
    caption = models.CharField(
        _("Caption for the post image"), max_length=200, blank=True)

    def __str__(self) -> str:
        return self.title


class UserLikePost(models.Model):
    user = models.ForeignKey(
        AccountUser, on_delete=models.CASCADE, blank=False, null=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.email} likes {self.post.title}"


class GeneralInformation(models.Model):
    user = models.OneToOneField(
        AccountUser, on_delete=models.CASCADE, blank=False)

    about_me = models.TextField(_("Introduction about the user"), blank=True)

    education = models.CharField(
        _("Name of the college"), max_length=500, blank=True)
    gender = models.CharField(
        _("Gender of user"), max_length=6, choices=GENDERS, blank=True)
    date_of_birth = models.DateField(_("Date of birth"), blank=True, null=True)
    organization = models.CharField(
        _("Organization name in which currently working."), max_length=500, blank=True)
    nationality = models.CharField(
        _("Nationality of the user"), choices=COUNTRY_NAMES, max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"General Information of {self.user.email}"


class PersonalInformation(models.Model):
    user = models.OneToOneField(
        AccountUser, on_delete=models.CASCADE, blank=False)

    profile_pic = models.ImageField(
        _("Profile pic of user"), upload_to="images", blank=True)
    first_name = models.CharField(
        _("First name of user"), max_length=300, blank=True)
    last_name = models.CharField(
        _("Last name of user"), max_length=300, blank=True)

    occupation = models.CharField(
        _("Occupation of user"), max_length=300, blank=True)
    status = models.CharField(
        _("Current status of user"), max_length=600, blank=True)
    location = models.CharField(
        _("location of user"), max_length=600, blank=True)
    home_address = models.TextField(
        _("Complete home address of user"), blank=True)
    phone_number = models.CharField(
        _("Phone number of user"), max_length=10, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Personal Information of {self.user.email}"


class Hobby(models.Model):
    title = models.CharField(_("Hobby title"), max_length=400)

    def __str__(self) -> str:
        return self.title


class Skill(models.Model):
    title = models.CharField(_("Skill title"), max_length=400)

    def __str__(self) -> str:
        return self.title


class ExtraInformation(models.Model):
    user = models.OneToOneField(
        AccountUser, on_delete=models.CASCADE, blank=False)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"ExtraInformation of {self.user.email}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        AccountUser, on_delete=models.CASCADE, blank=False, related_name="sender")
    receiver = models.ForeignKey(
        AccountUser, on_delete=models.CASCADE, blank=False, related_name="receiver")

    pending_status = models.BooleanField(default=True)
    Accept_status = models.BooleanField(default=False)
    Declined_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.sender.email} made friend request to {self.receiver.email}"
