from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Result, Candidate, Unit, Information, Statistics, Subunit
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def get_parent(unit):
    try:
        return Unit.objects.get(id=Subunit.objects.get(id_subunit_id=unit).id_unit_id)
    except ObjectDoesNotExist:
        return None

def get_ancestors(unit):
    anc = [unit]
    while True:
        unit = get_parent(unit)
        if unit is None:
            break
        else:
            anc.append(unit)
    return anc

def get_unit(request, name, typ):
    if typ == 'okreg':
        typ = 'okręg'
    if typ == 'wojewodztwo':
        typ = 'województwo'
    if typ == 'obwod':
        typ = 'obwód'
    print(name, typ)
    template = loader.get_template('unit.html')
    candidates = Candidate.objects.all()
    jednostka = Unit.objects.get(short_name=name, type=typ)
    rubryki = Information.objects.values_list('name', flat=True)
    stats = [item.value for item in Statistics.objects.filter(id_unit_id=jednostka)]
    ogolne = dict(zip(rubryki, stats))
    votes = [item.value for item in Result.objects.filter(id_unit_id=jednostka)]
    percentage = [0] * 12 if ogolne['Ważne głosy'] == 0 else [100 * vot / ogolne['Ważne głosy'] for vot in votes]
    res_dict = zip(candidates, votes, percentage)

    subunits = [Unit.objects.get(id=unit.id_subunit_id) for unit in Subunit.objects.filter(id_unit_id=jednostka)]
    links = [subunit.type + '/' + subunit.short_name for subunit in subunits]
    subunits = zip(subunits, links)

    ancestors = get_ancestors(jednostka)
    ancestors.reverse()
    menu_links = [unit.type + '/' + unit.short_name for unit in ancestors]
    ancestors = zip(ancestors, menu_links)

    print(ancestors)
    return HttpResponse(template.render({'res_dict': res_dict, 'ogolne': ogolne, 'subunits': subunits, 'ancestors': ancestors }))

def index(request):
    return get_unit(request, 'Polska', 'kraj')

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." %question_id)

def results(request, question_id):
    response = "You're loking at the results of the question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

