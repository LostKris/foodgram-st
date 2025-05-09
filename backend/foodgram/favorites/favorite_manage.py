from .models import FavoriteRecipe
from rest_framework.serializers import ValidationError
from django.shortcuts import get_list_or_404


def is_recipe_favorited(user, recipe):
    return recipe in [ fav.recipe for fav in user.favorite_recipes.all() ]

def add_favorite_recipe(user, recipe):
    if is_recipe_favorited(user, recipe):
        raise ValidationError('Рецепт уже добавлен в избранное')

    fav = FavoriteRecipe.objects.create(
        user=user,
        recipe=recipe,
    )
    return fav.recipe

def remove_favorite_recipe(user, recipe):
    if not is_recipe_favorited(user, recipe):
        raise ValidationError('Рецепт не находится в списке избранных')
    get_list_or_404(FavoriteRecipe, user=user, recipe=recipe)[0].delete()