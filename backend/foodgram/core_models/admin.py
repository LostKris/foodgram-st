from django.contrib import admin
from django import forms
from .models import Recipe, Ingredient, IngredientInRecipe


class IngredientInRecipeInline(admin.StackedInline):
    model = IngredientInRecipe
    extra = 1

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('measurement_unit',)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author','favorite_count',)
    filter = ('ingredients',)
    search_fields = ('name', 'author')
    fields = ('name', 'author', 'image', 'text', 'cooking_time','favorite_count',)
    readonly_fields = ('favorite_count',)
    inlines = (IngredientInRecipeInline,)

    def favorite_count(self, obj):
        return len(obj.favorited_in.all())

    favorite_count.short_description = 'Пользователей добавило в избранное'

class IngredientInRecipeAdmin(admin.ModelAdmin):
    pass

admin.site.empty_value_display = 'Не задано'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientInRecipe, IngredientInRecipeAdmin)