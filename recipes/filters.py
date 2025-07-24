import django_filters
from .models import Recipe, Region, Session, Category, Type

class RecipeFilter(django_filters.FilterSet):
    """
    Custom FilterSet for the Recipe model.
    """
    # --- Filtering for ManyToManyFields ---
    # These filters allow filtering by the name of the related object.
    # e.g., /api/list/?category=Salad&session=Lunch
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category__name',
        to_field_name='name',
        queryset=Category.objects.all(),
        conjoined=True, # Use AND logic for multiple categories
    )
    session = django_filters.ModelMultipleChoiceFilter(
        field_name='session__name',
        to_field_name='name',
        queryset=Session.objects.all(),
        conjoined=True, # Use AND logic for multiple sessions
    )
    type = django_filters.ModelMultipleChoiceFilter(
        field_name='type__name',
        to_field_name='name',
        queryset=Type.objects.all(),
        conjoined=True, # Use AND logic for multiple types
    )

    # --- Filtering for ForeignKey (One-to-Many) ---
    # e.g., /api/list/?region=Indian
    region = django_filters.ModelChoiceFilter(
        field_name='region__name',
        to_field_name='name',
        queryset=Region.objects.all()
    )

    # --- Filtering by Ingredient Name ---
    # This filter searches for recipes that contain a specific ingredient.
    # e.g., /api/list/?ingredients=Chicken
    ingredients = django_filters.CharFilter(
        field_name='recipe_ingredients__ingredient',
        lookup_expr='icontains' # Case-insensitive contains search
    )

    class Meta:
        model = Recipe
        fields = [
            'region',
            'session',
            'category',
            'type',
            'ingredients',
        ]
