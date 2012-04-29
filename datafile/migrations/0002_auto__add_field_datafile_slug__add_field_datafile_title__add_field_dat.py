# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DataFile.slug'
        db.add_column('datafile_datafile', 'slug',
                      self.gf('django_extensions.db.fields.AutoSlugField')(allow_duplicates=False, max_length=50, separator=u'-', blank=True, default='', populate_from='title', overwrite=False),
                      keep_default=False)

        # Adding field 'DataFile.title'
        db.add_column('datafile_datafile', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250),
                      keep_default=False)

        # Adding field 'DataFile.description'
        db.add_column('datafile_datafile', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'DataFile.source'
        db.add_column('datafile_datafile', 'source',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True),
                      keep_default=False)

        # Adding field 'DataFile.source_url'
        db.add_column('datafile_datafile', 'source_url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'DataFile.data'
        db.add_column('datafile_datafile', 'data',
                      self.gf('django.db.models.fields.TextField')(default='{}', blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'DataFile.slug'
        db.delete_column('datafile_datafile', 'slug')

        # Deleting field 'DataFile.title'
        db.delete_column('datafile_datafile', 'title')

        # Deleting field 'DataFile.description'
        db.delete_column('datafile_datafile', 'description')

        # Deleting field 'DataFile.source'
        db.delete_column('datafile_datafile', 'source')

        # Deleting field 'DataFile.source_url'
        db.delete_column('datafile_datafile', 'source_url')

        # Deleting field 'DataFile.data'
        db.delete_column('datafile_datafile', 'data')

    models = {
        'datafile.datafile': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'DataFile'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "'{}'", 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filetype': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'title'", 'overwrite': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['datafile']