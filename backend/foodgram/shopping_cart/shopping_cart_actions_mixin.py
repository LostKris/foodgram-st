from io import BytesIO

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers import RecipeMinifiedSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.http import FileResponse
from core_models.models import Recipe
from shopping_cart.shopping_cart_manage import (
    add_to_shopping_list,
    remove_from_shopping_list,
    get_shopping_cart_data,
)


class ShoppingCartActionsMixin:
    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="shopping_cart",
        url_name="shopping_cart",
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        match request.method:
            case "POST":
                serializer = RecipeMinifiedSerializer(
                    add_to_shopping_list(user, recipe)
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            case "DELETE":
                remove_from_shopping_list(user, recipe)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @action(
        methods=["get"],
        detail=False,
        url_path="download_shopping_cart",
        url_name="download_shopping_cart",
        permission_classes=(IsAuthenticated,),
    )
    def get_shopping_cart_file(self, request):
        user = request.user
        data = get_shopping_cart_data(user)
        str_data = ["Ингредиент,единица измерения,количество"] + [
            f"{k},{v}" for k, v in data.items()
        ]
        file_bytes = BytesIO("\n".join(str_data).encode("utf-8"))
        file_bytes.seek(0)

        return FileResponse(
            file_bytes,
            as_attachment=True,
            filename="shopping_list.csv",
            content_type="text/csv; charset=utf-8",
        )
