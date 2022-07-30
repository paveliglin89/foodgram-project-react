from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=255,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        return self.name
