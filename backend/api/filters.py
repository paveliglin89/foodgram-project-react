from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )
    author = filters.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )

    def get_is_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(in_favorite__user=self.request.user)
        return queryset.exclude(
            in_favorite__user=self.request.user
        )

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(
                in_shopping_list__user=self.request.user
            )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
