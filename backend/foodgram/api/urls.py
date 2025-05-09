from django.urls import path, include
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, UserViewSet

router = routers.SimpleRouter()
router.register("ingredients", IngredientViewSet)
router.register("recipes", RecipeViewSet)
router.register("users", UserViewSet)

urlpatterns = [path("", include(router.urls))]
