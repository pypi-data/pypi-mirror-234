from django import forms
from .models import Fileupload

class Fileform(forms.ModelForm):
    class Meta:
        model = Fileupload
        fields = ('Name', )
