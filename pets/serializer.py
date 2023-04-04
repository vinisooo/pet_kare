from rest_framework import serializers
from models import SexChoices
from groups.serializer import GroupSerializer
from traits.serializer import TraitsSerializer


class PetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField(min_value=0)
    weight = serializers.FloatField(min_value=0)
    sex = serializers.CharField(choices=SexChoices.choices)
    group = GroupSerializer()
    traits = TraitsSerializer(many=True)
