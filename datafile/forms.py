from django import forms

from datafile.models import DataFile

class UploadForm(forms.ModelForm):
    class Meta:
        model = DataFile
        fields = ('file',)
