from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import RecipeMinifiedSerializer
from core_models.models import Recipe
from favorites.favorite_manage import add_favorite_recipe, remove_favorite_recipe


class FavoriteActionsMixin:
    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='favorite',
        url_name='favorite',
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        match request.method:
            case 'POST':
                serializer = RecipeMinifiedSerializer(
                    add_favorite_recipe(user, recipe)
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            case 'DELETE':
                remove_favorite_recipe(user, recipe)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return None