from django import forms

from datafile.models import DataFile

class UploadForm(forms.ModelForm):
    class Meta:
        model = DataFile
        fields = ('title', 'file', 'filetype', 'description', 'source',
                  'source_url')
