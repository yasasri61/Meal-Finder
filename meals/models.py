from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Meal(models.Model):
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]

    name = models.CharField(max_length=160)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="meals")
    cuisine = models.CharField(max_length=80)
    image_url = models.URLField(blank=True)
    ingredients = models.JSONField(default=list)
    instructions = models.JSONField(default=list)
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default="Medium")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-rating", "name"]

    def __str__(self):
        return self.name
