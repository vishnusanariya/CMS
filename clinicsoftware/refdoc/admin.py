from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import RefDoc
# Register your models here.
@admin.register(RefDoc)
class RefDocadmin(ImportExportModelAdmin):
    list_display=('name','profession','address','contact')
