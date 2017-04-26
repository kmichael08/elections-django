from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Result, Candidate, Unit, Information, Statistics, Subunit
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
import re
from collections import OrderedDict
from elections.settings import MEDIA_ROOT
from django.contrib.auth import authenticate, login, logout
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

    name = re.sub('_', ' ', name)
    template = loader.get_template('president/unit.html')
    candidates = Candidate.objects.all()
    jednostka = get_object_or_404(Unit, short_name=name, type=typ)

    rubryki = Information.objects.values_list('name', flat=True).order_by('id')
    stats = [item.value for item in Statistics.objects.filter(id_unit_id=jednostka).order_by('id')]
    ogolne = OrderedDict(zip(rubryki, stats))
    votes = [item.value for item in Result.objects.filter(id_unit_id=jednostka)]
    percentage = [0] * 12 if ogolne['Ważne głosy'] == 0 else [100 * vot / ogolne['Ważne głosy'] for vot in votes]
    res_dict = zip(candidates, votes, percentage)

    subunits = [Unit.objects.get(id=unit.id_subunit_id) for unit in Subunit.objects.filter(id_unit_id=jednostka).order_by('id_subunit__name')]
    links = [subunit.type + '/' + subunit.short_name for subunit in subunits]
    links = [re.sub(' ', '_', item) for item in links]
    subunits = zip(subunits, links)

    ancestors = get_ancestors(jednostka)
    ancestors.reverse()
    menu_links = [unit.type + '/' + unit.short_name for unit in ancestors ]
    menu_links = [re.sub(' ', '_', item) for item in menu_links]

    ancestors = zip(ancestors, menu_links)

    try:
        pdf_file = jednostka.result_file.url
    except ValueError:
        pdf_file = ''

    return render(request, 'president/unit.html', {'res_dict': res_dict, 'ogolne': ogolne, 'subunits': subunits, 'ancestors': ancestors,
                                         'results_pdf' : pdf_file})

def index(request):
    return get_unit(request, 'Polska', 'kraj')

def get_pdf(request, filename):
    pdf_file = open(MEDIA_ROOT + filename, 'rb').read()
    return HttpResponse(pdf_file, content_type='application/pdf')

def django_login(request):
    print(request.POST)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/polska/')
    else:
        return redirect('/polska/')

def logout_view(request):
    logout(request)
    return redirect('/polska/')

def search(request):
    gmina = request.POST['gmina']
    successful = len(gmina) > 2
    gminy = Unit.objects.filter(type='gmina', name__contains=gmina)
    return render(request, 'president/lista_gmin.html', {'gminy':gminy, 'success' : successful})