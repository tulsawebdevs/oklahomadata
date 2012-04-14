from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel


settings.DATAFILES_SUBDIR = getattr(settings, 'DATAFILES_SUBDIR',
                                     'datafiles')
FILETYPE_CHOICES = (
    ('csv', 'CSV'),
    ('json', 'JSON'),
    ('xml', 'XML'))


class DataFile(TimeStampedModel):
    file = models.FileField(upload_to=settings.DATAFILES_SUBDIR)
    filetype = models.CharField(max_length=20, choices=FILETYPE_CHOICES,
                                null=True, blank=True)

    def __unicode__(self):
        return unicode(self.file.name)
