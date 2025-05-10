from rest_framework import viewsets, filters

from ..serializers import IngredientSerializer
from core_models.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


    
