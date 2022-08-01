from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilter
from .models import Favorite, Recipe, RecipeIngredient, ShoppingList
from .permissions import IsAuthorOrAdminPermission
from .serializers import (RecipeCreateUpdateSerializer, RecipeSerializer,
                          ShortRecipeSerializer)
from ingredients.models import Ingredient
from users.pagination import CustomPageNumberPagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    @action(detail=True, methods=('post', 'delete'))
    def favorite(self, request, pk=None):
        action_for_create_or_delete(self, request, flag='Favorite', pk=None)


    @action(detail=True, methods=('post', 'delete'))
    def shopping_cart(self, request, pk=None):
        action_for_create_or_delete(self, request, flag='ShoppingList', pk=None)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        buy_list = RecipeIngredient.objects.filter(
            recipe__shoppinglist__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(ingredient_total=Sum('amount'))
        buy_list_text = 'Список покупок:\n'
        for item in buy_list:
            ingredient = Ingredient.objects.get(pk=item['ingredient'])
            amount = item['amount']
            buy_list_text += (
                f'#{ingredient.name}, {amount} {ingredient.measurement_unit}\n'
            )
        response = HttpResponse(buy_list_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping-list.txt'
        )
        return response


def action_for_create_or_delete(self, request, flag, pk=None):
    user = self.request.user
    recipe = get_object_or_404(Recipe, pk=pk)

    if self.request.method == 'POST':
        if flag == 'Favorite':
            Favorite.objects.create(user=user, recipe=recipe)
        elif flag == 'ShoppingList':
            ShoppingList.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(
            recipe,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if self.request.method == 'DELETE':
        if flag == 'Favorite':
            obj = get_object_or_404(Favorite, user=user, recipe=recipe)
            obj.delete()
        if flag == 'ShoppingList':
            obj = get_object_or_404(ShoppingList, user=user, recipe=recipe)
            obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
