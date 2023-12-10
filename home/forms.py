from django import forms

class PostCreationForm(forms.Form):
    
    title = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'class':'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}))

    content = forms.CharField(widget=forms.Textarea(attrs={'class':'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5', 'rows':'5'}))
    
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class':'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}))
    
    caption = forms.CharField(max_length=400, required=False, widget=forms.TextInput(attrs={'class':'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}))