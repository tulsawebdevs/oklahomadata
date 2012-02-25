from django.views.generic.edit import FormView

from datafile.forms import UploadForm
from django.conf import settings


class UploadView(FormView):
    form_class = UploadForm
    success_url = "/"
    template_name = "datafile/upload.html"

    def form_valid(self, form):
        f = self.request.FILES['csv_file']
        destination = open("%s/%s" % (settings.MEDIA_ROOT, f.name), 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        return super(UploadView, self).form_valid(form)
