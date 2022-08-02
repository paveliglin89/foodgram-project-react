from django_filters.rest_framework import filters, FilterSet

from recipes.models import Recipe


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    author = filters.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )

    def is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites=self.request.user)
        return queryset

    def is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_list=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
