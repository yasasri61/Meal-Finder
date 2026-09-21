
from django.test import TestCase
from django.urls import reverse
from .models import Category, Meal

class MealFinderTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Test", slug="test")
        self.meal = Meal.objects.create(
            name="Test Pasta", description="A test meal", category=category,
            cuisine="Italian", ingredients=["pasta", "tomato"],
            instructions=["Cook it"], cooking_time=20, difficulty="Easy", rating=4.5
        )

    def test_home_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_search_finds_meal(self):
        response = self.client.get(reverse("meal_list"), {"search": "Pasta"})
        self.assertContains(response, "Test Pasta")

    def test_api_returns_meals(self):
        response = self.client.get("/api/meals/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Pasta")
