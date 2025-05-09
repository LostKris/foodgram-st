from django.contrib.auth import get_user_model
from django.db import models


class Subscription(models.Model):
    """Модель подписки пользователя на другого"""
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='подписчик'
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='prevent_self_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
