from django.db import models
from django.forms import fields
from .models import UploadImage
from django import forms

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadImage
        fields = '__all__'