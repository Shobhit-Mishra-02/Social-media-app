from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AccountUser

class AccountUserAdmin(UserAdmin):
    list_display = ("email","is_staff", "is_active", "is_superuser")

admin.site.register(AccountUser, AccountUserAdmin)
