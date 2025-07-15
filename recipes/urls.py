from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import RecipeStep
from .views import (
    RecipeViewSet,
    IngredientViewSet,
    RegionViewSet,
    SessionViewSet,
    CategoryViewSet,
    TypeViewSet,
    RecipeListView,
    RecipeDetailView,
    FilterOptionsView,
    OptionsView,
    StepsViewSet,
    MyRecipeCreateView,
    MyRecipeListView,
    MyRecipeUpdateView,
    MyRecipeDeleteView,
    RecipeStepCreateView,
    RecipeStepUpdateView,
    RecipeStepDeleteView,
    TopRecipesListView,
    FeedbackCreateView
)

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'types', TypeViewSet)
router.register(r'steps', StepsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', RecipeListView.as_view(), name='recipe-list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path("filters/", FilterOptionsView.as_view(), name="filter-options"),
    path("options/", OptionsView.as_view(), name="options"),
    path("top-recipes/", TopRecipesListView.as_view(), name="top-recipes"),

    path("feedback/", FeedbackCreateView.as_view(), name="feedback-create"),
    
    path("my-recipes/", MyRecipeListView.as_view(), name="my-recipes"),
    path('create/', MyRecipeCreateView.as_view(), name='recipe-create'),
    path('<int:pk>/update/',MyRecipeUpdateView.as_view(), name='recipe-update'),
    path('<int:pk>/delete/', MyRecipeDeleteView.as_view(), name='recipe-delete'),

    path('<int:recipe_id>/steps/create/', RecipeStepCreateView.as_view(), name='step-create'),
    path('steps/<int:pk>/update/', RecipeStepUpdateView.as_view(), name='step-update'),
    path('steps/<int:pk>/delete/', RecipeStepDeleteView.as_view(), name='step-delete'),
]
