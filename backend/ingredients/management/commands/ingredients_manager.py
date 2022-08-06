import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """
    Импорт ингредиентов из файла CSV.
    """

    def handle(self, *args, **kwargs):
        with open(
                'ingredients/data/ingredients.csv', 'r',
                encoding='UTF-8'
        ) as ingredients:
            for row in csv.reader(ingredients):
                if len(row) == 2:
                    Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
