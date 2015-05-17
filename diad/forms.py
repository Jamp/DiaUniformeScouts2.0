from django import forms

class UploadForm(forms.Form):
    album = forms.IntegerField()
    url = forms.ImageField()