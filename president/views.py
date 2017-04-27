from django.http import HttpResponse
from .models import Result, Candidate, Unit, Information, Statistics, Subunit
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
import re
from collections import OrderedDict
from elections.settings import MEDIA_ROOT
from django.contrib.auth import authenticate, login, logout


def get_parent(unit):
    try:
        return Unit.objects.get(id=Subunit.objects.get(id_subunit_id=unit).id_unit_id)
    except ObjectDoesNotExist:
        return None

""""""
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
    name = re.sub('_', ' ', name)
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

    diagram = [['kandydat', 'głosy']]
    for cand, votes, percentage in res_dict:
        diagram.append([cand.str(), votes])

    template = 'president/obwod.html' if typ=='obwód' else 'president/unit.html'

    return render(request, template, {'res_dict': res_dict, 'ogolne': ogolne, 'subunits': subunits, 'ancestors': ancestors,
                                         'results_pdf' : pdf_file, 'kandydaci':candidates, 'diagram': diagram})

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

def upload_pdf(request, name):
    # Handle file upload
    pdf_file = request.FILES['pdf_obwod']

    unit = Unit.objects.get(type='obwód', short_name=name)
    unit.result_file='obwód_' + name
    unit.save()

    with open(MEDIA_ROOT + '/' + 'obwód_' + name , 'wb+') as destination:
        for chunk in pdf_file.chunks():
            destination.write(chunk)

    print(request.path)
    return redirect('/polska/obwód/' + name)

def edit_votes(request, name):
    print(request.POST)
    cand = request.POST['kandydat']
    print(cand, name)
    res = Result.objects.get(id_unit__short_name=name, id_cand_id=cand)
    res.value = request.POST['votes']
    res.save()
    return redirect('/polska/obwód/' + name)

