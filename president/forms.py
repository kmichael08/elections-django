from django import forms
from .models import Candidate

class SearchGminaForm(forms.Form):
    gmina = forms.CharField(max_length=20, min_length=3,
                            widget=forms.TextInput(attrs={'placeholder': 'Podaj gminę'}))


class UploadFileForm(forms.Form):
    pdf_obwod = forms.FileField()


class EditVotesForm(forms.Form):
    votes = forms.IntegerField(min_value=0)
    choice = [(cand.id, cand) for cand in Candidate.objects.all()]
    kandydat = forms.ChoiceField(choice)


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20, label=None,
                               widget=forms.TextInput(attrs={'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput, min_length=3)