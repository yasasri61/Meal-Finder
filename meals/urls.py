from django.urls import path
from .views import home, meal_list, meal_detail, ingredient_finder

urlpatterns = [
    path("", home, name="home"),
    path("meals/", meal_list, name="meal_list"),
    path("meals/<int:pk>/", meal_detail, name="meal_detail"),
    path("ingredient-finder/", ingredient_finder, name="ingredient_finder"),
]
