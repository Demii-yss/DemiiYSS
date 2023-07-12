from django import forms
from .models import UploadImage


class UploadImageForm(forms.ModelForm):
    class Meta:
        models = UploadImage
        fields = '__all__'
