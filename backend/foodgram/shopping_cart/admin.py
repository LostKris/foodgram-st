from django.contrib import admin

from .models import ShoppingCart


class ShoppingCartInline(admin.StackedInline):
    model = ShoppingCart
    extra = 0


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    pass


admin.site.register(ShoppingCart, ShoppingCartAdmin)
