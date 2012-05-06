from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from datafile.views import (DataFileDetails, DataFileDownload, DataFilesList,
                            UploadView)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^dataupload/', include('dataupload.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name="home/index.html"),
        name='home'),
    url(r'^datafiles/$', DataFilesList.as_view(), name='datafile_list'),
    url(r'^datafiles/(?P<slug>[a-z0-9\-]+)/$', DataFileDetails.as_view(),
        name='datafile_details'),
    url(r'^datafiles/(?P<slug>[a-z0-9\-]+)/download/'
        r'(?P<download_type>[a-z]+)/$',
        DataFileDownload.as_view(), name='datafile_download'),
    url(r'^upload/$', UploadView.as_view(), name='upload_form'),
    (r'^boundary/', include('boundaryservice.urls')),
    (r'^boundary/$', include('boundary_demo.urls')),
)
