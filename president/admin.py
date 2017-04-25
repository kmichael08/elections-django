from django.contrib import admin

# Register your models here.
from .models import Result

from president.models import Document
admin.site.register(Document)


class ResultAdmin(admin.ModelAdmin):
    list_display = ('id_cand', 'id_unit')
    list_filter = ['id_cand']
    search_fields = ['id_unit__type', 'id_unit__name']

admin.site.register(Result, ResultAdmin)