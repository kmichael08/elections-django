from django.test import TestCase, RequestFactory
from .models import Unit, Subunit, Candidate, Statistics, Result, Information
from .views import get_parent, get_ancestors, index
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, User

class TestAncestor(TestCase):
    def test_parent(self):
        unit = Unit(type='gmina', name='Szubin', short_name='22222')
        unit.save()

        obwod = Unit(type='obwód', name='Szkoła', short_name='obw333')
        obwod.save()

        sub = Subunit(id_unit=unit, id_subunit=obwod)
        sub.save()

        self.assertEqual(get_parent(obwod), unit)

    def test_ancestors(self):
        powiat = Unit(type='powiat', name='nakielski', short_name='1212313')
        powiat.save()

        gmina = Unit(type='gmina', name='Szubin', short_name='233123')
        gmina.save()

        obwod = Unit(type='obwód', name='Szkoła', short_name='12314')
        obwod.save()

        obwod2 = Unit(type='obwód', name='Remiza', short_name='134555555')
        obwod2.save()

        Subunit(id_unit=powiat, id_subunit=gmina).save()
        Subunit(id_unit=gmina, id_subunit=obwod).save()
        Subunit(id_unit=gmina, id_subunit=obwod2).save()

        self.assertEqual(get_ancestors(obwod)[1:], get_ancestors(obwod2)[1:])
        self.assertEqual(get_ancestors(obwod), [obwod, gmina, powiat])


class TestModels(TestCase):
    def test_candidate(self):
        cand=Candidate(name='George', second_name='Walker', surname='Bush')
        self.assertEqual(cand.str(), 'George Walker Bush')

    def test_result(self):
        cand=Candidate(name='George', surname='Bush')
        cand.save()
        unit=Unit(type='kraj', name='Niemcy', short_name='Ger')
        unit.save()
        res=Result(id_unit=unit, id_cand=cand, value=1000)
        res.save()
        self.assertEqual(res.__str__(), 'kraj Niemcy, George Bush')

    def test_information(self):
        unit = Unit(type='województwo', name='kujawsko-pomorskie', short_name='kujawsko-pomorskie')
        unit.save()

        info = Information(name='Liczba ważnych głosów')
        info.save()

        stat = Statistics(id_unit=unit, id_information=info, value=3.123)
        stat.save()

        self.assertEqual(stat.value, 3.123)

class TestViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='daniel', email='a@a.pl', password='haslo')

    def createData(self):
        info = Information(name='Ważne głosy')
        info.save()

        unit = Unit(type='kraj', name='Polska', short_name='Polska')
        unit.save()

        stat = Statistics(id_information=info, id_unit=unit, value=123)
        stat.save()
        return unit

    def test_index(self):
        self.createData()

        request = self.factory.get('/polska')

        request.user = self.user

        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_index2(self):
        unit = self.createData()

        cand = Candidate(name='Jan', surname='Kowalski')
        cand.save()

        res = Result(id_unit=unit, id_cand=cand, value=331122)
        res.save()

        request = self.factory.get('/polska')

        request.user = self.user

        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jan Kowalski', count=2)

