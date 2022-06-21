from django_filters import FilterSet
from django_filters import rest_framework as filter
from recipes.models import Recipe, RecipeUsers


class RecipeFilter(FilterSet):
    is_favorite = filter.NumberFilter(method='get_is_favorite')
    in_is_shopping_cart = filter.NumberFilter(
        method='get_in_is_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['is_favorite', 'in_is_shopping_cart']

    def get_is_favorite(self, queryset, name, value):
        if value == 1:
            if self.request.user.is_authenticated:
                obj = RecipeUsers.objects.filter(user=self.request.user)
                if obj.count() != 0:
                    queryset = obj[0].users_favorite.all()
        return queryset

    def get_in_is_shopping_cart(self, queryset, name, value):
        if value == 1:
            if self.request.user.is_authenticated:
                obj = RecipeUsers.objects.filter(user=self.request.user)
                if obj.count() != 0:
                    queryset = obj[0].users_shopping.all()
        return queryset
