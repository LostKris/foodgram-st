from django.contrib import admin

from favorites.admin import FavoriteRecipeInline
from shopping_cart.admin import ShoppingCartInline
from subscriptions.admin import UserSubscriptionInline
from .models import User

class UserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'username',)
    list_display = ('username', 'email')
    inlines = (UserSubscriptionInline, FavoriteRecipeInline, ShoppingCartInline,)
    exclude = ('password',)
    readonly_fields = ('date_joined', 'last_login',)

admin.site.register(User, UserAdmin)
