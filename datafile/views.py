from django.views.generic.edit import *

from datafile.forms import UploadForm
import settings

class UploadView(FormView):
    form_class = UploadForm
    success_url = "/"
    template_name = "datafile/upload.html"

    def form_valid(self, form):
        def handle_uploaded_file(f):
            destination = open("%s/%s" % (MEDIA_ROOT, f.name), 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

        handle_uploaded_file(self.request.FILES['file'])

        print(form.cleaned_data)
        return super(UploadView, self).form_valid(form)
