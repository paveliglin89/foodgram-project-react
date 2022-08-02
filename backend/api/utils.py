from django.shortcuts import get_object_or_404

from recipes.models import RecipeIngredient
from ingredients.models import Ingredient


def create_recepie_ingredients(ingredients, recipe):
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
    RecipeIngredient.objects.bulk_create(recepie_ingredients)
    return recepie_ingredients
