from csv import DictWriter
import StringIO

from django.contrib import messages
from django.http import Http404, HttpResponse
from django.views.generic import DetailView, FormView, ListView, View
from django.views.generic.detail import SingleObjectMixin

from datafile.forms import UploadForm
from datafile.models import DataFile


class DataFileDetails(DetailView):
    model = DataFile
    template_name = 'datafile/file_details.html'


class DataFileDownload(SingleObjectMixin, View):
    model = DataFile
    file_field = 'file'

    def get(self, request, *args, **kwargs):
        dl_type = self.kwargs.get('download_type', '')
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if dl_type == 'raw':
            try:
                file_obj = getattr(self.object, self.file_field)
            except AttributeError:
                raise Http404
            data = file_obj.read()
            filetype = self.object.filetype
            if self.object.filetype == 'json':
                mimetype = 'application/json'
            else:
                assert self.object.filetype == 'csv'
                mimetype = 'text/csv'
        elif dl_type == 'json':
            if self.object.data:
                data = str(self.object.data)
                mimetype = 'application/json'
                filetype = 'json'
            else:
                raise Http404
        elif dl_type == 'csv':
            if self.object.data:
                f = StringIO.StringIO()
                dw = DictWriter(
                    f, [field['fieldname']
                        for field in self.object.data['meta']['columns']])
                dw.writeheader()
                dw.writerows(self.object.data['data'])
                data = f.getvalue()
                f.close()
                mimetype = 'text/csv'
                filetype = 'csv'
            else:
                raise Http404
        else:
            raise Http404
        response =  HttpResponse(data, content_type=mimetype)
        response['Content-Disposition'] = 'filename=%s.%s' % (
            self.object.slug, filetype)
        return response


class DataFilesList(ListView):
    model = DataFile
    template_name = 'datafile/file_list.html'


class UploadView(FormView):
    form_class = UploadForm
    success_url = '/'
    template_name = 'datafile/upload.html'

    def form_valid(self, form, *args, **kwargs):
        form.save()
        messages.success(self.request, 'File saved successfully')
        return super(UploadView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request,
                         'Failed to upload file. Please try again.')
        return super(UploadView, self).form_invalid(form, *args, **kwargs)
