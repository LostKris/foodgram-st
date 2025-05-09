from django.contrib import admin

from .models import Subscription


class UserSubscriptionInline(admin.StackedInline):
    model = Subscription
    extra = 0
    fk_name = "user"


admin.site.register(Subscription)
