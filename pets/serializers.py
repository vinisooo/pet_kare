from rest_framework import serializers
from .models import SexChoices
from groups.serializers import GroupSerializer
from traits.serializers import TraitsSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField(min_value=0)
    weight = serializers.FloatField(min_value=0)
    sex = serializers.ChoiceField(choices=SexChoices.choices)
    group = GroupSerializer()
    traits = TraitsSerializer(many=True)
