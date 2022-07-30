from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Имя тэга',
    )
    color = models.CharField(
        max_length=255,
        verbose_name='Цвет тэга',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug тэга',
    )

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self):
        return self.name
