from django import forms

class PostCreationForm(forms.Form):
    title = forms.CharField(max_length=300)
    content = forms.CharField(widget=forms.Textarea)
    
    image = forms.ImageField(required=False)
    caption = forms.CharField(max_length=400, required=False)