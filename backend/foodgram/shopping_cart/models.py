from django.contrib.auth import get_user_model
from django.db import models

from core_models.models import Recipe


class ShoppingCart(models.Model):
    """Модель-связка для 'корзины'"""
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_shopping_carts',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'рецепт в корзине'
        verbose_name_plural = 'рецепты в корзине'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в корзине пользователя {self.user}'
