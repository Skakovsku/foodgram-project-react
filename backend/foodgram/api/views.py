from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from recipes.models import Tag
from recipes.serializers import TagSerializer


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
