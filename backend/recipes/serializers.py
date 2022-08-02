from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from drf_base64.fields import Base64ImageField
from rest_framework import exceptions, serializers

from .models import Favorite, Recipe, RecipeIngredient, ShoppingList
from .utils import create_recepie_ingredients, update_recepie_ingredients
from ingredients.models import Ingredient
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer

User = get_user_model()


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit',)


class CreateUpdateRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=(MinValueValidator(1, message='Кол-во должно быть > 0.'),)
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipeingredient_set'
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingList.objects.filter(user=user, recipe=obj).exists()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    def validate(self, data):
        user = self.context.get("request").user
        new_recipe = self.initial_data.get("recipe")
        if (
            Favorite.objects.all()
            .filter(user=user, recipe=new_recipe)
            .exists()
        ):
            raise exceptions.ValidationError("Этот рецепт уже в избранном")
        recipe = data.get("recipe")
        if (
            ShoppingList.objects.all()
            .filter(user=user, recipe=recipe)
            .exists()
        ):
            raise exceptions.ValidationError("Этот рецепт уже в вашей корзине")
        return data


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = CreateUpdateRecipeIngredientSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        validators=(MinValueValidator(
            1, message='Время приготовления должно быть > 0.'
        ),)
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    def validate_tags(self, value):
        if not value:
            raise exceptions.ValidationError(
                'Нужно добавить хотя бы один тэг.'
            )
        return value

    def validate_ingredients(self, value):
        if not value:
            raise exceptions.ValidationError(
                'Нужно добавить хотя бы один ингредиент.'
            )
        ingredients = [item['id'] for item in value]
        for ingredient in ingredients:
            if ingredients.count(ingredient) > 1:
                raise exceptions.ValidationError(
                    'У рецепта не может быть два одинаковых ингредиента.'
                )
            if int(ingredient['amount']) <= 0:
                raise exceptions.ValidationError(
                    'Количество ингредиентов должно быть больше нуля.'
                )
        return value

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        create_recepie_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.set(tags)
        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:
            instance.ingredients.clear()
            update_recepie_ingredients(ingredients, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data

    class Meta:
        model = Recipe
        exclude = ('pub_date',)


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
