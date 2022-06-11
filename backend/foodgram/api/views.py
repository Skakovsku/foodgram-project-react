from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from rest_framework.filters import SearchFilter
from recipes.models import Product, Tag
from .serializers import IngredientSerializer, TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        obj = Tag.objects.filter(pk=kwargs['pk'])
        if len(obj) == 0:
            raise exceptions.NotFound(
                {'detail': 'Страница не найдена.'}
            )
        return super().retrieve(request, *args, **kwargs)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter,)  # Если db='Postgrees', то нечувствителен к регистру
    search_fields = ('^name',)
