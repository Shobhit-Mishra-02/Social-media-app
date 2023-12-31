from django import forms
from django.forms import ModelForm, CharField, Textarea, TextInput, DateField, Select, DateInput
from home.models import GeneralInformation, GENDERS, COUNTRY_NAMES


class PostCreationForm(forms.Form):

    title = forms.CharField(max_length=300, widget=forms.TextInput(attrs={
                            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-1.5 mb-2', 'placeholder': 'title of your post...'}), label_suffix="")

    content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-1.5 mb-2', 'rows': '2', 'placeholder': 'text content of your post...'}), label_suffix="")

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
                             'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-1.5 mb-2 hidden'}), label_suffix="")

    caption = forms.CharField(max_length=400, required=False, widget=forms.TextInput(
        attrs={'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-1.5 mb-2', 'placeholder': 'add caption here...'}), label='Image caption', label_suffix="")


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
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5",
                "placeholder": "Thomas Jeff High School, Stanford University"
            }),
            "gender": Select(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"
            },
                choices=GENDERS),
            "date_of_birth": DateInput(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5",
                "type": "date"
            },
                format="%Y-%m-%d"),
            "organization": TextInput(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5",
                "placeholder": "Themesberg LLC"
            }),
            "nationality": Select(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5",
            },
                choices=COUNTRY_NAMES)
        }
