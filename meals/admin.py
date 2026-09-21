from django.contrib import admin
from .models import Category, Meal

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "cuisine", "cooking_time", "difficulty", "rating")
    list_filter = ("category", "cuisine", "difficulty")
    search_fields = ("name", "description", "cuisine")
