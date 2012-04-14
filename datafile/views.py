from django.views.generic.edit import FormView

from django.contrib import messages

from datafile.forms import UploadForm


class UploadView(FormView):
    form_class = UploadForm
    success_url = "/"
    template_name = "datafile/upload.html"

    def form_valid(self, form, *args, **kwargs):
        form.save()
        messages.success(self.request, 'File saved successfully')
        return super(UploadView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request,
                         'Failed to upload file. Please try again.')
        return super(UploadView, self).form_invalid(form, *args, **kwargs)
