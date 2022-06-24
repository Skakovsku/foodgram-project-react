from django_filters import FilterSet
from django_filters import rest_framework as filter

from recipes.models import Recipe, RecipeUsers, Tag


class RecipeFilter(FilterSet):
    is_favorited = filter.NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = filter.NumberFilter(
        method='get_is_in_shopping_cart'
    )
    tags = filter.CharFilter(method='get_tags')

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'author', 'is_in_shopping_cart', 'tags']

    def get_is_favorited(self, queryset, name, value):
        if value == 1:
            if self.request.user.is_authenticated:
                obj = RecipeUsers.objects.filter(user=self.request.user)
                if obj.count() != 0:
                    queryset = obj[0].users_favorite.all()
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value == 1:
            if self.request.user.is_authenticated:
                obj = RecipeUsers.objects.filter(user=self.request.user)
                if obj.count() != 0:
                    queryset = obj[0].users_shopping.all()
        return queryset

    def get_tags(self, queryset, name, value):
        print(value)
        tags_obj = Tag.objects.filter(slug=value)
        if tags_obj.count() == 0:
            return queryset
        queryset = Recipe.objects.filter(tags=tags_obj[0])
        return queryset
