# Generated by Django 4.0.6 on 2022-07-31 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
        ('ingredients', '0001_initial'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecipeIngredients',
            new_name='RecipeIngredient',
        ),
        migrations.RenameModel(
            old_name='RecipeTags',
            new_name='RecipeTag',
        ),
    ]
