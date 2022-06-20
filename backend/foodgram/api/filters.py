from django_filters import FilterSet
from django_filters import rest_framework as filter
from recipes.models import Recipe, RecipeUsers


class RecipeFilter(FilterSet):
    is_favorite = filter.CharFilter(method='get_is_favorite')

    class Meta:
        model = Recipe
        fields = ['is_favorite']

    def get_is_favorite(self, queryset, name, value):
        if value == 1:
            if self.request.user.is_authenticated:
                obj = RecipeUsers.objects.get(user=self.request.user)
                queryset = obj.users_favorite.all()
        return queryset
