from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from favorites.favorite_actions_mixin import FavoriteActionsMixin
from shopping_cart.shopping_cart_actions_mixin import ShoppingCartActionsMixin
from ..serializers import RecipeSerializer, RecipeCreateSerializer
from ..filters import RecipeFilter
from core_models.models import Recipe
from foodgram import permissions


class RecipeViewSet(
    viewsets.ModelViewSet, FavoriteActionsMixin, ShoppingCartActionsMixin
):
    queryset = Recipe.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = RecipeFilter
    ordering_fields = ('-pub_date',)
    permission_classes = (permissions.IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "create" or self.action == "partial_update":
            return RecipeCreateSerializer
        return RecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        output_serializer = RecipeSerializer(
            serializer.instance,
            context={"request": request},
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        output_serializer = RecipeSerializer(
            serializer.instance, context={"request": request}
        )
        return Response(output_serializer.data)

    @action(
        methods=["get"],
        detail=True,
        url_path="get-link",
        url_name="get-link",
    )
    def get_short_link(self, request, pk):
        url = str.format("{host}/s/{pk}", host=request.get_host(), pk=pk)
        return Response(
            data={
                "short-link": url,
            }
        )
