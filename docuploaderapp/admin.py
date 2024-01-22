from django.contrib import admin
from django.forms import TextInput, Textarea
from .models import *

# Register your models here.

class DocumentAdmin(admin.ModelAdmin):
    model = Document
    list_display = ('client_name', 'company_name')
    search_fields = ['client_name', 'company_name']
admin.site.register(Document, DocumentAdmin)


class ParaplannerAdmin(admin.ModelAdmin):
    model = Paraplanner
    search_fields = ['paraplanner']
admin.site.register(Paraplanner, ParaplannerAdmin)


class StatusAdmin(admin.ModelAdmin):
    model = Status
    search_fields = ['status']
admin.site.register(Status, StatusAdmin)