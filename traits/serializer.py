from rest_framework import serializers
from pets.serializer import PetSerializer


class TraitsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    pets = PetSerializer(many=True)
    created_at = serializers.DateTimeField(read_only=True)
