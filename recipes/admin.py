from django.contrib import admin
from .models import Recipe, Region, Session, Category, RecipeStep, Type, Feedback, \
    RecipeIngredient  # Import RecipeIngredient


# New Inline for RecipeIngredient
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1  # How many extra empty ingredient forms to show


class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'is_published')
    list_filter = ('author', 'region', 'session', 'category', 'type')
    search_fields = ('title', 'description', 'author__username')
    inlines = [RecipeIngredientInline, RecipeStepInline]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email', 'message')


# Keep these registrations as they are
admin.site.register(Region)
admin.site.register(Session)
admin.site.register(Category)
admin.site.register(RecipeStep)
admin.site.register(Type)