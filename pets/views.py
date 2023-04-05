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

        group, created = Group.objects.get_or_create(
            scientific_name__iexact=group["scientific_name"], defaults=group
        )

        traits = serializer.validated_data.pop("traits")
        pet = Pet.objects.create(**serializer.validated_data, group=group)
        for trait_data in traits:
            trait, created = Trait.objects.get_or_create(
                name__iexact=trait_data["name"], defaults=trait_data
            )
            pet.traits.add(trait)

        response_data = PetSerializer(pet).data
        return Response(response_data, status.HTTP_201_CREATED)

    def get(self, request):
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class PetsDetailView(APIView):
    def get(self, request, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found"}, status.HTTP_404_NOT_FOUND)
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found"}, status.HTTP_404_NOT_FOUND)
        pet.delete()

        return Response(model_to_dict(pet), status.HTTP_204_NO_CONTENT)

    def patch(self, request, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return Response({"detail": "Not found"}, status.HTTP_404_NOT_FOUND)

        serializer = PetSerializer(pet, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        traits = serializer.validated_data.pop("traits", None)
        group = serializer.validated_data.pop("group", None)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        if group:
            group, _ = Group.objects.get_or_create(
                scientific_name__iexact=group["scientific_name"], defaults=group
            )
            pet.group = group

        if traits:
            pet.traits.clear()
            for trait_data in traits:
                trait, _ = Trait.objects.get_or_create(
                    name__iexact=trait_data["name"], defaults=trait_data
                )
                pet.traits.add(trait)

        pet.save()

        response_data = PetSerializer(pet).data
        return Response(response_data, status.HTTP_200_OK)
