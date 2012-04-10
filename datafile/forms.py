from django import forms

class UploadForm(forms.Form):
    csv_file = forms.FileField()
