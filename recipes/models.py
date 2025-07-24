from django.db import models
from django.conf import settings

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='recipes', null=True, blank=True)
    session = models.ManyToManyField(Session, related_name='recipes', blank=True)
    category = models.ManyToManyField(Category, related_name='recipes', blank=True)
    type = models.ManyToManyField(Type, related_name='recipes', blank=True)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_recipes', blank=True)
    saved_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='saved_recipes', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=True)
    servings = models.IntegerField(default=1)
    prep_time = models.IntegerField(help_text="Prep time in minutes", default=0)
    cook_time = models.IntegerField(help_text="Cook time in minutes", default=0)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE, related_name="recipe_ingredients")
    ingredient = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ingredient} - {self.quantity}"


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    step_no = models.PositiveIntegerField()
    instruction = models.TextField()
    timer = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='step_images/', blank=True, null=True)

    class Meta:
        ordering = ['step_no']

    def __str__(self):
        return f"Step {self.step_no} for {self.recipe.title}"


class Feedback(models.Model):
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.email}"
