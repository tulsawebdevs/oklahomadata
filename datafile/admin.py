from django.contrib import admin

from datafile.models import DataFile


class DataFileAdmin(admin.ModelAdmin):
    model = DataFile

    def parse_data(self, request, queryset):
        for f in queryset:
            f.parse_data()

    actions = (parse_data,)

admin.site.register(DataFile, DataFileAdmin)
