from django.contrib import admin

from .models import FavoriteRecipe


class FavoriteRecipeInline(admin.StackedInline):
    model = FavoriteRecipe
    extra = 0


admin.site.register(FavoriteRecipe)
