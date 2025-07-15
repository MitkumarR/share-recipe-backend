from django.contrib import admin
from .models import Recipe, Ingredient, Region, Session, Category, RecipeStep, Type, Feedback

class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'is_published')
    list_filter = ('author', 'region', 'session', 'category', 'type')
    search_fields = ('title', 'description', 'author__username')
    inlines = [RecipeStepInline]
    filter_horizontal = ('ingredients',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email', 'message')
    
admin.site.register(Ingredient)
admin.site.register(Region)
admin.site.register(Session)
admin.site.register(Category)
admin.site.register(RecipeStep)
admin.site.register(Type)