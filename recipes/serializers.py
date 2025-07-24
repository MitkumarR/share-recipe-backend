from rest_framework import serializers
from .models import (
    Recipe, Region, Session, Category,
    RecipeStep, Type, Feedback, RecipeIngredient
)


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


from rest_framework import serializers
from .models import (
    Recipe, RecipeIngredient, RecipeStep,
    Region, Session, Category, Type
)


class RecipeIngredientSerializer(serializers.Serializer):
    ingredient = serializers.CharField()
    quantity = serializers.CharField()


class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ['step_no', 'instruction', 'timer', 'image']



class RecipeSerializer(serializers.ModelSerializer):
    # These fields are for input only and won't be shown in the response.
    ingredients = RecipeIngredientSerializer(many=True, write_only=True)
    steps = RecipeStepSerializer(many=True, write_only=True)
    region = serializers.CharField(write_only=True)
    session = serializers.ListField(child=serializers.CharField(), write_only=True)
    category = serializers.ListField(child=serializers.CharField(), write_only=True)
    type = serializers.ListField(child=serializers.CharField(), write_only=True)

    # These fields are for output only.
    total_likes = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Recipe
        fields = [
            'id', 'author', 'title', 'description', 'image',
            'ingredients', 'region', 'session', 'category', 'type',
            'steps', 'servings', 'prep_time', 'cook_time',
            'created_at', 'updated_at', 'total_likes', 'is_published'
        ]

    def create(self, validated_data):
        # Pop the nested data from the validated data
        ingredients_data = validated_data.pop('ingredients')
        steps_data = validated_data.pop('steps', [])
        region_name = validated_data.pop('region')
        session_names = validated_data.pop('session')
        category_names = validated_data.pop('category')
        type_names = validated_data.pop('type')

        # --- MODIFIED: Use get_or_create for Region ---
        # It returns a tuple (object, created_boolean), we only need the object.
        region, _ = Region.objects.get_or_create(name=region_name)

        # Create the recipe instance with the simple fields
        recipe = Recipe.objects.create(region=region, **validated_data)

        # --- MODIFIED: Use get_or_create for ManyToMany fields ---
        for name in session_names:
            session, _ = Session.objects.get_or_create(name=name)
            recipe.session.add(session)

        for name in category_names:
            category, _ = Category.objects.get_or_create(name=name)
            recipe.category.add(category)

        for name in type_names:
            type_obj, _ = Type.objects.get_or_create(name=name)
            recipe.type.add(type_obj)

        # Create the related Ingredient and Step objects
        for item in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **item)

        for step in steps_data:
            RecipeStep.objects.create(recipe=recipe, **step)

        return recipe

    def update(self, instance, validated_data):
        # Pop the nested data if it exists
        ingredients_data = validated_data.pop('ingredients', None)
        steps_data = validated_data.pop('steps', None)
        region_name = validated_data.pop('region', None)
        session_names = validated_data.pop('session', None)
        category_names = validated_data.pop('category', None)
        type_names = validated_data.pop('type', None)

        # --- MODIFIED: Use get_or_create for update logic as well ---
        if region_name:
            instance.region, _ = Region.objects.get_or_create(name=region_name)

        if session_names:
            instance.session.clear()
            for name in session_names:
                session, _ = Session.objects.get_or_create(name=name)
                instance.session.add(session)

        if category_names:
            instance.category.clear()
            for name in category_names:
                category, _ = Category.objects.get_or_create(name=name)
                instance.category.add(category)

        if type_names:
            instance.type.clear()
            for name in type_names:
                type_obj, _ = Type.objects.get_or_create(name=name)
                instance.type.add(type_obj)

        # Handle ingredients and steps update (delete old, create new)
        if ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            for item in ingredients_data:
                RecipeIngredient.objects.create(recipe=instance, **item)

        if steps_data is not None:
            instance.steps.all().delete()
            for step in steps_data:
                RecipeStep.objects.create(recipe=instance, **step)

        # Update the remaining simple fields on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

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
    session = serializers.StringRelatedField(many=True)
    category = serializers.StringRelatedField(many=True)
    type = serializers.StringRelatedField(many=True)
    ingredients = serializers.SerializerMethodField()
    steps = RecipeStepSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        return [
            {"ingredient": ri.ingredient, "quantity": ri.quantity}
            for ri in obj.recipe_ingredients.all()
        ]

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'email', 'message', 'created_at']
