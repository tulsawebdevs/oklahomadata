from csv import DictReader
from json import loads
import logging

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.fields.json import JSONField


settings.DATAFILES_SUBDIR = getattr(settings, 'DATAFILES_SUBDIR',
                                    'datafiles')
logger = logging.getLogger('okdata')


class DataFile(TimeStampedModel):
    slug = AutoSlugField(populate_from='title')
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    source = models.CharField(max_length=250, blank=True)
    source_url = models.URLField(blank=True)
    file = models.FileField(upload_to=settings.DATAFILES_SUBDIR)
    filetype_choices = (
        ('csv', 'CSV'),
        ('json', 'JSON'))
    filetype = models.CharField(max_length=20, choices=filetype_choices,
                                null=True, blank=True)
    data = JSONField(blank=True)

    def __unicode__(self):
        return unicode(self.title)

    def build_meta_from_dict(self, data):
        fieldnames = set()
        for row in data:
            for fieldname in row.keys():
                fieldnames.add(fieldname)
        return {'columns': [{'fieldname': self.transform_fieldname(field)}
                            for field in fieldnames],
                'records': len(data)}

    @property
    def filedata(self):
        try:
            return self._filedata
        except AttributeError:
            if self.filetype == 'csv':
                self._filedata = DictReader(self.file)
            elif self.filetype == 'json':
                self._filedata = loads(self.file.read())
            return self._filedata

    def parse_csv(self):
        if self.validate_csv():
            data = list()
            for row in self.filedata:
                data.append([{self.transform_fieldname(fieldname): value}
                             for fieldname, value in row.items()])

            meta = {
                'columns': [{'fieldname': self.transform_fieldname(fieldname)}
                            for fieldname in self.filedata.fieldnames],
                'records': len(data),
            }
            return {'meta': meta, 'data': data}
        else:
            logger.warning('File is not a parsable csv structure.')

    def parse_data(self):
        parsed_data = None
        if self.filetype == 'csv':
            parsed_data = self.parse_csv()
        elif self.filetype == 'json':
            parsed_data = self.parse_json()

        if parsed_data:
            self.data = parsed_data
            self.save()
            return self.data

    def parse_json(self):
        if self.validate_json():
            data = {}
            if (isinstance(self.filedata, dict) and
                    'data' in self.filedata.keys() and
                    isinstance(self.filedata['data'][0], dict)):
                data = self.filedata
                if not 'meta' in self.filedata.keys():
                    data['meta'] = {}
                data['meta'].update(self.build_meta_from_dict(data['data']))
            elif isinstance(self.filedata, list):
                data['data'] = self.filedata
                data['meta'] = self.build_meta_from_dict(self.filedata)

            return data
        else:
            logger.warning('File is not a parsable json structure.')

    def transform_fieldname(self, fieldname):
        return slugify(fieldname.lower()).replace('-', '_')

    def validate_csv(self):
        return True
        return False

    def validate_data(self):
        if self.filetype == 'csv':
            valid = self.validate_csv()
        elif self.filetype == 'json':
            valid = self.validate_json()

        return valid

    def validate_json(self):
        try:
            if (isinstance(self.filedata, dict) and
                    'data' in self.filedata.keys() and
                    isinstance(self.filedata['data'][0], dict)) or (
                        isinstance(self.filedata, list)):
                return True
        except:
            pass
        return False

@receiver(models.signals.post_save, sender=DataFile)
def post_create_handler(sender, instance, created, **kwargs):
    if created:
        instance.parse_data()
