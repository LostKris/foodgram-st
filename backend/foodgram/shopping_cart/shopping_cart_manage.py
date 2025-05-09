from .models import ShoppingCart
from rest_framework.serializers import ValidationError
from django.shortcuts import get_list_or_404


def is_in_shopping_list(user, recipe):
    return recipe in [ item.recipe for item in user.shopping_cart.all() ]

def add_to_shopping_list(user, recipe):
    if is_in_shopping_list(user, recipe):
        raise ValidationError('Рецепт уже добавлен в корзину')

    fav = ShoppingCart.objects.create(
        user=user,
        recipe=recipe,
    )
    return fav.recipe

def remove_from_shopping_list(user, recipe):
    if not is_in_shopping_list(user, recipe):
        raise ValidationError('Рецепт не находится в корзине')
    get_list_or_404(ShoppingCart, user=user, recipe=recipe)[0].delete()

def get_shopping_cart_data(user):
    data = {}
    for item in user.shopping_cart.all():
        recipe = item.recipe
        for ingredient_in_recipe in recipe.ingredient_in_recipe.all():
            ingredient = ingredient_in_recipe.ingredient
            amount = ingredient_in_recipe.amount
            key = f'{ingredient.name},{ingredient.measurement_unit}'
            data[key] = data.get(key, 0) + amount
    return data