from rest_framework import serializers
from .models import Recipe, Ingredient, Region, Session, Category, RecipeStep, Type, Feedback


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']


class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ['step_no', 'instruction', 'timer', 'image']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), many=True)
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    session = serializers.PrimaryKeyRelatedField(
        queryset=Session.objects.all())
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all())
    steps = RecipeStepSerializer(many=True, read_only=True)
    total_likes = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Recipe
        fields = [
            'id', 'author', 'title', 'description', 'type', 'image',
            'ingredients', 'region', 'session', 'category',
            'steps', 'servings', 'prep_time', 'cook_time',
            'created_at', 'updated_at', 'total_likes'
        ]


class RecipeListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'image', 'likes', 'author']

    def get_likes(self, obj):
        return obj.total_likes()


class RecipeDetailSerializer(serializers.ModelSerializer):
    region = serializers.StringRelatedField()
    session = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    type = serializers.StringRelatedField()
    ingredients = serializers.StringRelatedField(many=True)
    steps = RecipeStepSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'email', 'message', 'created_at']