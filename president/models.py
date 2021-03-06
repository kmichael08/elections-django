from django.db import models
from elections.settings import MEDIA_ROOT

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    second_name = models.CharField(max_length=120, null=True)

    def str(self):
        if self.second_name is None:
            return self.name + ' ' + self.surname
        else:
            return self.name + ' ' + self.second_name + ' ' + self.surname

    def __str__(self):
        return self.str()

def update_filename(instance, filename):
    format = instance.type + '_' + instance.short_name
    return format

class Unit(models.Model):
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=300)
    short_name = models.CharField(max_length=100)
    def __str__(self):
        return self.type + ' ' + self.name
    result_file = models.FileField(upload_to=update_filename, null=True)


class Information(models.Model):
    name = models.CharField(max_length=150)

class Result(models.Model):
    id_cand = models.ForeignKey(Candidate)
    id_unit = models.ForeignKey(Unit)
    value = models.IntegerField()
    def __str__(self):
        return Unit.objects.get(id=self.id_unit_id).__str__() + ', ' + Candidate.objects.get(id=self.id_cand_id).__str__()

    def str(self):
        return self.__str__()

class Statistics(models.Model):
    id_information = models.ForeignKey(Information)
    id_unit = models.ForeignKey(Unit)
    value = models.FloatField()

class Subunit(models.Model):
    id_unit = models.ForeignKey(Unit, related_name='unit')
    id_subunit = models.ForeignKey(Unit, related_name='subunit')

class Document(models.Model):
    docfile = models.FileField(upload_to=MEDIA_ROOT)