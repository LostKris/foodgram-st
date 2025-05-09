from django.contrib.auth import get_user_model
from django.db import models

from core_models.models import Recipe


# Create your models here.
class FavoriteRecipe(models.Model):
    """Модель-связка для отметки избранных рецептов"""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="favorite_recipes",
        verbose_name="пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorited_in",
        verbose_name="рецепт",
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_favorite",
            )
        ]

    def __str__(self):
        return f"{self.recipe} в избранном у {self.user}"
