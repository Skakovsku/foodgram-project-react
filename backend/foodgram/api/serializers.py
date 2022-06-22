from rest_framework.serializers import ModelSerializer, SerializerMethodField
from recipes.models import Ingredient, Product, Recipe, Tag
from users.serializers import CurrentUserSerializer
from .fields import Base64ImageField


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    name = SerializerMethodField(read_only=True)
    measurement_unit = SerializerMethodField(read_only=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)

    def get_name(self, obj):
        return obj.product.name

    def get_measurement_unit(self, obj):
        return obj.product.measurement_unit


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CurrentUserSerializer(read_only=True)
    ingredients = IngredientSerializer(read_only=True, many=True)
    image = Base64ImageField(max_length=None, use_url=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time',)

    def get_is_favorited(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return True

    def get_is_in_shopping_cart(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return True
