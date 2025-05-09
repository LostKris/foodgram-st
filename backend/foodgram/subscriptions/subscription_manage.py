from .models import Subscription
from rest_framework.serializers import ValidationError
from django.shortcuts import get_list_or_404


def is_subscribed(user, author):
    return author in [sub.author for sub in user.subscriptions.all()]


def subscribe(user, author):
    if user == author:
        raise ValidationError("Нельзя подписаться на самого себя")
    if is_subscribed(user, author):
        raise ValidationError("Подписка уже оформлена")
    sub = Subscription.objects.create(
        user=user,
        author=author,
    )
    return sub.author


def unsubscribe(user, author):
    if user == author:
        raise ValidationError("Нельзя отписаться от самого себя")
    if not is_subscribed(user, author):
        raise ValidationError("Подписка на этого пользователя не оформлена")
    get_list_or_404(Subscription, user=user, author=author)[0].delete()
