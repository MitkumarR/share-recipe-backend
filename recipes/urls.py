from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import RecipeStep
from .views import (
    RecipeViewSet,
    RegionViewSet,
    SessionViewSet,
    CategoryViewSet,
    TypeViewSet,

    RecipeListView,
    RecipeDetailView,
    TopRecipesListView,
    RecipeLikeToggleView,
    RecipeSaveToggleView,
    SavedRecipeListView,

    FilterOptionsView,
    OptionsView,
    StepsViewSet,

    MyRecipeCreateView,
    MyRecipeListView,
    MyRecipeUpdateView,
    MyRecipeDeleteView,

    FeedbackCreateView, CommentListCreateView, CommentRetrieveUpdateDestroyView
)

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'types', TypeViewSet)
router.register(r'steps', StepsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('list/', RecipeListView.as_view(), name='recipe-list'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path("top-recipes/", TopRecipesListView.as_view(), name="top-recipes"),

    path('recipe/<int:pk>/like/', RecipeLikeToggleView.as_view(), name='recipe-like-toggle'),
    path('recipe/<int:pk>/save/', RecipeSaveToggleView.as_view(), name='recipe-save-toggle'),
    path('saved-recipes/', SavedRecipeListView.as_view(), name='saved-recipe-list'),

    path('recipe/<int:recipe_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),

    path("filters/", FilterOptionsView.as_view(), name="filter-options"),
    path("options/", OptionsView.as_view(), name="options"),

    path("feedback/", FeedbackCreateView.as_view(), name="feedback-create"),
    
    path("my-recipes/", MyRecipeListView.as_view(), name="my-recipes"),
    path('create/', MyRecipeCreateView.as_view(), name='recipe-create'),
    path('<int:pk>/update/',MyRecipeUpdateView.as_view(), name='recipe-update'),
    path('<int:pk>/delete/', MyRecipeDeleteView.as_view(), name='recipe-delete'),


]
