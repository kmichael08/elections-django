from django.contrib import admin

# Register your models here.
from .models import Result, Unit


class ResultAdmin(admin.ModelAdmin):
    list_display = ('id_cand', 'typ', 'name')
    def typ(self, obj):
        return obj.id_unit.type
    def name(self, obj):
        return obj.id_unit.name
    list_filter = ['id_cand']
    search_fields = ['id_unit__type', 'id_unit__name']

    def get_queryset(self, request):
        qs = super(ResultAdmin, self).get_queryset(request)
        return qs.filter(id_unit__type='obwód')

admin.site.register(Result, ResultAdmin)

class UnitAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'result_file')
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super(UnitAdmin, self).get_queryset(request)
        return qs.filter(type='obwód')

admin.site.register(Unit, UnitAdmin)
