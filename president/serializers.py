from rest_framework import serializers
from .models import Unit, Candidate


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('type', 'name', 'short_name', 'result_file')


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ('name', 'surname', 'second_name')

