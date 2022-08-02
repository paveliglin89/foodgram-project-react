from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes import serializers

from .models import Recipe, RecipeIngredient
from ingredients.models import Ingredient


def get_recepie_ingredients_list(ingredients, recipe):
    recepie_ingredients = []
    for ingredient in ingredients:
        ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])
        amount = ingredient['amount']
        recepie_ingredient = RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        )
        recepie_ingredients.append(recepie_ingredient)
    return recepie_ingredients


def create_recepie_ingredients(ingredients, recipe):
    recepie_ingredients = get_recepie_ingredients_list(ingredients, recipe)
    RecipeIngredient.objects.bulk_create(recepie_ingredients)


def update_recepie_ingredients(ingredients, recipe):
    recepie_ingredients = get_recepie_ingredients_list(ingredients, recipe)
    RecipeIngredient.objects.bulk_update(recepie_ingredients)


def action_create_or_delete(self, request, model, pk=None):
    user = self.request.user
    recipe = get_object_or_404(Recipe, pk=pk)

    if self.request.method == 'POST':
        model.objects.create(user=user, recipe=recipe)
        serializer = serializers.ShortRecipeSerializer(
            recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if self.request.method == 'DELETE':
        obj = get_object_or_404(model, user=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
