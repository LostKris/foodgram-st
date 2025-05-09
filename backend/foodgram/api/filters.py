from django_filters import rest_framework as filters
from core_models.models import Recipe
from favorites.favorite_manage import is_recipe_favorited
from shopping_cart.shopping_cart_manage import is_in_shopping_list


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method="filter_is_in_shopping_cart",
    )

    class Meta:
        model = Recipe
        fields = ["author"]

    def filter_is_favorited(self, queryset, name, value):
        if value:
            user = self.request.user
            if user.is_authenticated:
                favorited_ids = [
                    recipe.id
                    for recipe in queryset
                    if is_recipe_favorited(user, recipe)
                ]
                return queryset.filter(id__in=favorited_ids)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            user = self.request.user
            if user.is_authenticated:
                shopping_cart_ids = [
                    recipe.id
                    for recipe in queryset
                    if is_in_shopping_list(user, recipe)
                ]
                return queryset.filter(id__in=shopping_cart_ids)
        return queryset
