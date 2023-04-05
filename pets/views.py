from django.shortcuts import render
from django.forms.models import model_to_dict
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import PetSerializer

from .models import Pet
from groups.models import Group
from traits.models import Trait


class PetsView(APIView, PageNumberPagination):
    def post(self, request):
        serializer = PetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response((serializer.errors), status.HTTP_400_BAD_REQUEST)

        group = serializer.validated_data.pop("group")

        group, created = Group.objects.get_or_create(**group)

        traits = serializer.validated_data.pop("traits")
        pet = Pet.objects.create(**serializer.validated_data, group=group)
        for trait_data in traits:
            trait, created = Trait.objects.get_or_create(name=trait_data["name"])
            pet.traits.add(trait)

        return Response(model_to_dict(pet), status.HTTP_201_CREATED)

    def get(self, request):
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
