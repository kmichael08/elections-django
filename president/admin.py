from django.contrib import admin

# Register your models here.
from .models import Result, Unit, Candidate

class ResultAdmin(admin.ModelAdmin):
    list_display = ('id_cand', 'typ', 'name')
    def typ(self, obj):
        return obj.id_unit.type
    def name(self, obj):
        return obj.id_unit.name
    list_filter = ['id_cand', 'id_unit__type']
    search_fields = ['id_unit__type', 'id_unit__name']

admin.site.register(Result, ResultAdmin)

class UnitAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'short_name')
    search_fields = ['name']
    list_filter = ['type']
    fields = ('type', 'name', 'short_name')


admin.site.register(Unit, UnitAdmin)

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'surname', 'second_name')
    search_fields = ['name', 'surname', 'second_name']

admin.site.register(Candidate, CandidateAdmin)


class Obwod(Unit):
    class Meta:
        proxy = True

    objects = Unit()


class PdfAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'result_file')
    search_fields = ['name']
    list_filter = ['type']
    list_display_links = ('name',)

    def get_queryset(self, request):
        qs = super(PdfAdmin, self).get_queryset(request)
        return qs.filter(type = "obwód")


admin.site.register(Obwod, PdfAdmin)
