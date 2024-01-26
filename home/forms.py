from django import forms
from django.forms import ModelForm, CharField, Textarea, TextInput, DateField, Select, DateInput, FileInput
from home.models import GeneralInformation, GENDERS, COUNTRY_NAMES, PersonalInformation, Post

COMMON_DESIGN = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"


class PostCreationForm(ModelForm):

    class Meta:
        model = Post

        fields = ["title", "content", "image", "caption"]

        widgets = {
            "title": TextInput(attrs={
                "class": COMMON_DESIGN,
                "placeholder": "title of your post..."
            }),
            "content": Textarea(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-1.5 mb-2",
                "placeholder": "text content of your post...",
                "rows": "4"
            }),
            "image": FileInput(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-1.5 mb-2 hidden"
            }),
            "caption": TextInput(attrs={
                "class": COMMON_DESIGN,
                "placeholder": "add caption here..."
            })
        }


class GeneralInformationForm(ModelForm):

    class Meta:
        model = GeneralInformation
        fields = ["about_me", "education", "gender",
                  "date_of_birth", "organization", "nationality"]

        widgets = {
            "about_me": Textarea(attrs={
                "rows": "4",
                "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "92 Miles Drive, Newark, NJ 07103, California, United States of America"
            }),
            "education": TextInput(attrs={
                "class": COMMON_DESIGN,
                "placeholder": "Thomas Jeff High School, Stanford University"
            }),
            "gender": Select(attrs={
                "class": COMMON_DESIGN
            },
                choices=GENDERS),
            "date_of_birth": DateInput(attrs={
                "class": COMMON_DESIGN,
                "type": "date"
            },
                format="%Y-%m-%d"),
            "organization": TextInput(attrs={
                "class": COMMON_DESIGN,
                "placeholder": "Themesberg LLC"
            }),
            "nationality": Select(attrs={
                "class": COMMON_DESIGN,
            },
                choices=COUNTRY_NAMES)
        }


class PersonalInformationForm(ModelForm):

    class Meta:
        model = PersonalInformation

        fields = ["profile_pic", "first_name", "last_name", "occupation",
                  "status", "location", "home_address", "phone_number"]

        widgets = {
            "profile_pic": FileInput(attrs={
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-full p-1.5 mb-2 hidden",
                "type": "file",
            }),
            "first_name": TextInput(attrs={
                "class": COMMON_DESIGN,
                "placeholder": "John"
            }),
            "last_name": TextInput(attrs={
                "class": COMMON_DESIGN,
                "placeholder": "Smith"
            }),
            "occupation": TextInput(attrs={
                "class": COMMON_DESIGN,
                "placeholder": "Front-end developer"
            }),
            "status": TextInput(attrs={
                "class": COMMON_DESIGN,
                "placeholder": "working for society :)"
            }),
            "location": TextInput(attrs={
                "class": COMMON_DESIGN,
                "placeholder": "New delhi, Delhi"
            }),
            "home_address": Textarea(attrs={
                "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "92 Miles Drive, Newark, NJ 07103, California, United States of America",
                "rows": "4"
            }),
            "phone_number": TextInput(attrs={
                "class": COMMON_DESIGN,
                "placeholder": "123 456 789",
                "pattern": "[0-9]{10}"
            })
        }
