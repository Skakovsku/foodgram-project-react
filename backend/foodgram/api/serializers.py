from rest_framework.serializers import ModelSerializer
from recipes.models import Product, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
