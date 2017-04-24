from django.db import models

# Create your models here.

class Question(models.Model):
    question_test = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_test

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

class Unit(models.Model):
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=300)
    short_name = models.CharField(max_length=100)

class Information(models.Model):
    name = models.CharField(max_length=150)

class Result(models.Model):
    id_cand = models.ForeignKey(Candidate)
    id_information = models.ForeignKey(Information)
    id_unit = models.ForeignKey(Unit)

class Statistics(models.Model):
    id_information = models.ForeignKey(Information)
    id_unit = models.ForeignKey(Unit)

class Subunit(models.Model):
    id_unit = models.ForeignKey(Unit, related_name='unit')
    id_subunit = models.ForeignKey(Unit, related_name='subunit')