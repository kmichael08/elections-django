from django.http import HttpResponse, JsonResponse
from .models import Result, Candidate, Unit, Information, Statistics, Subunit
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
import re
from collections import OrderedDict
from elections.settings import MEDIA_ROOT
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SearchGminaForm, UploadFileForm, EditVotesForm, LoginForm
from .serializers import UnitSerializer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib import messages


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


@require_http_methods(["GET", "POST"])
def get_unit(request, name, typ):
    candidates = Candidate.objects.all()

    rubryki = Information.objects.values_list('name', flat=True).order_by('id')

    template = 'president/obwod.html' if typ=='obwód' else 'president/unit.html'

    if request.method == 'POST':
        search_form = SearchGminaForm(request.POST)
        upload_form = UploadFileForm(request.POST)
        edit_votes_form = EditVotesForm(request.POST)
        login_form = LoginForm(request.POST)
    else:
        search_form = SearchGminaForm()
        upload_form = UploadFileForm()
        edit_votes_form = EditVotesForm()
        login_form = LoginForm()

    return render(request, template, {'search_form': search_form, 'upload_form': upload_form,
                                      'edit_votes_form': edit_votes_form, 'login_form': login_form,
                                      'rubryki': rubryki, 'candidates': candidates,
                                      'typ': typ, 'name': name})


@require_GET
def get_unit_data(request, name, typ):
    name = re.sub('_', ' ', name)
    candidates = Candidate.objects.all()

    jednostka = get_object_or_404(Unit, short_name=name, type=typ)
    stats = [item.value for item in Statistics.objects.filter(id_unit_id=jednostka).order_by('id')]

    rubryki = Information.objects.values_list('name', flat=True).order_by('id')
    ogolne = OrderedDict(zip(rubryki, stats))
    votes = [item.value for item in Result.objects.filter(id_unit_id=jednostka)]
    percentage = [0] * Candidate.objects.count() if ogolne['Ważne głosy'] == 0 else [100 * vot / ogolne['Ważne głosy'] for vot in votes]

    subunits = [Unit.objects.get(id=unit.id_subunit_id) for unit in
                Subunit.objects.filter(id_unit_id=jednostka).order_by('id_subunit__name')]

    links = [subunit.type + '/' + subunit.short_name for subunit in subunits]
    links = [re.sub(' ', '_', item) for item in links]

    subunits = [UnitSerializer(unit).data for unit in subunits]

    ancestors = get_ancestors(jednostka)
    ancestors.reverse()

    menu_links = [unit.type + '/' + unit.short_name for unit in ancestors]
    menu_links = [re.sub(' ', '_', item) for item in menu_links]

    ancestors = [UnitSerializer(unit).data for unit in ancestors]

    try:
        pdf_file = jednostka.result_file.url
    except ValueError:
        pdf_file = ''

    diagram = [['kandydat', 'głosy']]
    for cand, vote in zip(candidates, votes):
        diagram.append([cand.str(), vote])

    content = {'percentage': percentage, 'votes': votes, 'stats': stats,
                'results_pdf': pdf_file, 'diagram': diagram, 'ancestors': ancestors, 'menu_links': menu_links,
                'subunits': subunits, 'links': links, 'is_obwod': typ == 'obwód'}

    return JsonResponse(content)


@require_http_methods(["GET", "POST"])
def index(request):
    return get_unit(request, 'Polska', 'kraj')


def get_pdf(request, filename):
    pdf_file = open(MEDIA_ROOT + filename, 'rb').read()
    return HttpResponse(pdf_file, content_type='application/pdf')


@require_POST
def django_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
    return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='/polska/')
def logout_view(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])


@require_POST
def search(request):
    return render(request, 'president/lista_gmin.html', {'gmina': request.POST['gmina']})


@require_POST
def lista_gmin(request):
    gmina = request.POST['gmina']
    gminy = Unit.objects.filter(type='gmina', name__contains=gmina)
    gminy = [UnitSerializer(gmina).data for gmina in gminy]
    return JsonResponse({'gminy': gminy})


@require_POST
@login_required(login_url='/polska')
def upload_pdf(request, name):
    # Handle file upload
    pdf_file = request.FILES['pdf_obwod']

    unit = get_object_or_404(Unit, type='obwód', short_name=name)
    unit.result_file='obwód_' + name
    unit.save()

    with open(MEDIA_ROOT + '/' + 'obwód_' + name , 'wb+') as destination:
        for chunk in pdf_file.chunks():
            destination.write(chunk)

    return redirect('/polska/obwód/' + name)


@require_POST
@login_required(login_url='/polska')
def edit_votes_dynamic(request, name):
    cand = request.POST['kandydat']
    votes = request.POST['votes']
    res = get_object_or_404(Result, id_unit__short_name=name, id_cand_id=cand)
    res.value = votes
    res.save()
    return JsonResponse({'name': name})

