from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Result, Candidate, Unit, Information, Statistics, Subunit
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
import re
from president.models import Document
from president.forms import DocumentForm
from django.core.urlresolvers import reverse
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

    rubryki = Information.objects.values_list('name', flat=True)
    stats = [item.value for item in Statistics.objects.filter(id_unit_id=jednostka)]
    ogolne = dict(zip(rubryki, stats))
    votes = [item.value for item in Result.objects.filter(id_unit_id=jednostka)]
    percentage = [0] * 12 if ogolne['Ważne głosy'] == 0 else [100 * vot / ogolne['Ważne głosy'] for vot in votes]
    res_dict = zip(candidates, votes, percentage)

    subunits = [Unit.objects.get(id=unit.id_subunit_id) for unit in Subunit.objects.filter(id_unit_id=jednostka)]
    links = [subunit.type + '/' + subunit.short_name for subunit in subunits]
    links = [re.sub(' ', '_', item) for item in links]
    subunits = zip(subunits, links)

    ancestors = get_ancestors(jednostka)
    ancestors.reverse()
    menu_links = [unit.type + '/' + unit.short_name for unit in ancestors ]
    menu_links = [re.sub(' ', '_', item) for item in menu_links]

    ancestors = zip(ancestors, menu_links)
    return HttpResponse(template.render({'res_dict': res_dict, 'ogolne': ogolne, 'subunits': subunits, 'ancestors': ancestors }))

def index(request):
    return get_unit(request, 'Polska', 'kraj')


def lista(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render(request, 'president/list.html', {'documents': documents, 'form': form})
