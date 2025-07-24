from django.db.models import F
from rest_framework import viewsets, permissions, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import (
    Recipe, Region, Session, Category,
    RecipeStep, Type, Feedback, RecipeIngredient, Comment
)
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    RecipeSerializer, RecipeIngredientSerializer, RegionSerializer,
    SessionSerializer, CategorySerializer, RecipeListSerializer,
    RecipeDetailSerializer, RecipeStepSerializer, TypeSerializer,
    FeedbackSerializer, CommentSerializer
)

from django_filters.rest_framework import DjangoFilterBackend
from .filters import RecipeFilter # Import the custom filter class


# Helper function to check ownership
def user_is_recipe_author(user, recipe_id):
    return Recipe.objects.filter(id=recipe_id, author=user).exists()

# ========== Public Recipes ==========

class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = RecipeListSerializer
    # Keep the backends, but we will replace filterset_fields
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_class = RecipeFilter

    # Keep search and ordering fields as they are
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'likes__count']  # Note: ordering by likes is more efficient this way

class TopRecipesListView(generics.ListAPIView):
    queryset = Recipe.objects.filter(is_published=True)[:6]
    serializer_class = RecipeListSerializer


class RecipeDetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.filter(is_published=True)
    serializer_class = RecipeDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view_count efficiently without race conditions
        instance.view_count = F('view_count') + 1
        instance.save(update_fields=['view_count'])
        instance.refresh_from_db()  # Refresh to get the updated value
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# ========== Comments ==========

class CommentListCreateView(generics.ListCreateAPIView):
    """
    View to list all comments for a recipe or create a new one.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Filter comments based on the recipe_pk from the URL
        recipe_pk = self.kwargs['recipe_pk']
        return Comment.objects.filter(recipe_id=recipe_pk)

    def perform_create(self, serializer):
        # Automatically associate the comment with the recipe and the user
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_pk'])
        serializer.save(author=self.request.user, recipe=recipe)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a single comment.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # Use the custom permission to ensure only authors can edit/delete
    permission_classes = [IsOwnerOrReadOnly]

# ========== Like/Unlike a Recipe ==========

class RecipeLikeToggleView(APIView):
    """
    View to like or unlike a recipe.
    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # Get the recipe object, or return 404 if not found
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        # Check if the user has already liked the recipe
        if user in recipe.likes.all():
            # If liked, remove the like (unlike)
            recipe.likes.remove(user)
            liked = False
        else:
            # If not liked, add the like
            recipe.likes.add(user)
            liked = True

        # Return a response with the current like status and total likes
        return Response({
            'liked': liked,
            'total_likes': recipe.total_likes()
        }, status=status.HTTP_200_OK)


# ========== Save/Unsave a Recipe ==========

class RecipeSaveToggleView(APIView):
    """
    View to save or unsave a recipe for the logged-in user.
    Requires authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        if user in recipe.saved_by.all():
            # If already saved, remove it from saved list
            recipe.saved_by.remove(user)
            saved = False
        else:
            # If not saved, add it to the saved list
            recipe.saved_by.add(user)
            saved = True

        return Response({'saved': saved}, status=status.HTTP_200_OK)


class SavedRecipeListView(generics.ListAPIView):
    """
    View to list all recipes saved by the currently authenticated user.
    """
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return all recipes from the 'saved_recipes' related manager
        return self.request.user.saved_recipes.all().order_by('-created_at')


# ========== Filter Options ==========

class FilterOptionsView(APIView):
    def get(self, request):
        data = {
            "types": list(Type.objects.values("name")),
            "categories": list(Category.objects.values("name")),
            "regions": list(Region.objects.values("name")),
            "sessions": list(Session.objects.values("name")),
            # --- ADDED THIS LINE ---
            "ingredients": list(RecipeIngredient.objects.values_list('ingredient', flat=True).distinct().order_by('ingredient')),
        }
        return Response(data, status=status.HTTP_200_OK)


class OptionsView(APIView):
    def get(self, request):
        data = {
            "types": list(Type.objects.values("name")),
            "categories": list(Category.objects.values("name")),
            "regions": list(Region.objects.values("name")),
            # Corrected this line to provide a distinct list of ingredient names
            "ingredients": list(RecipeIngredient.objects.values_list('ingredient', flat=True).distinct().order_by('ingredient')),
            "sessions": list(Session.objects.values("name")),
        }
        return Response(data, status=status.HTTP_200_OK)

# ========== ReadOnly ViewSets ==========

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeDetailSerializer
        return RecipeSerializer

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class SessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class StepsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecipeStep.objects.all()
    serializer_class = RecipeStepSerializer


# ========== User's Own Recipes (CRUD) ==========

class MyRecipeCreateView(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print("Received data:", self.request.data)
        serializer.save(author=self.request.user)


class MyRecipeListView(generics.ListAPIView):
    serializer_class = RecipeListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'type__name', 'session__name', 'category__name']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'total_likes']

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user).order_by('-created_at')


class MyRecipeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)


class MyRecipeDeleteView(generics.DestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)


# ========== Feedback ==========

class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.AllowAny]
