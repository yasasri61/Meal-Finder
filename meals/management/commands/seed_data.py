from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from meals.models import Category, Meal

DATA = [
    ("Indian", "indian", [
        ("Chicken Biryani", "Fragrant basmati rice layered with spiced chicken, herbs and caramelized onion.", "Indian", 50, "Medium", 4.9,
         ["chicken", "basmati rice", "onion", "tomato", "garlic", "ginger", "yogurt", "biryani spices"],
         ["Marinate chicken with yogurt and spices.", "Cook rice until partly done.", "Prepare the masala and sear the chicken.", "Layer rice over chicken and cook covered.", "Garnish with herbs and serve."]),
        ("Paneer Tikka", "Smoky yogurt-marinated paneer with peppers and onions.", "Indian", 30, "Easy", 4.7,
         ["paneer", "yogurt", "bell pepper", "onion", "garam masala", "lemon"],
         ["Mix yogurt with spices.", "Marinate paneer and vegetables.", "Thread onto skewers.", "Grill until lightly charred.", "Serve with lemon."]),
        ("Vegetable Pulao", "Aromatic one-pot rice loaded with seasonal vegetables.", "Indian", 30, "Easy", 4.6,
         ["basmati rice", "carrot", "peas", "beans", "onion", "cumin"],
         ["Rinse the rice.", "Saute spices and vegetables.", "Add rice and water.", "Cover and simmer until fluffy.", "Rest for five minutes and serve."]),
    ]),
    ("Italian", "italian", [
        ("Creamy Alfredo Pasta", "Silky pasta tossed in parmesan cream sauce with garlic.", "Italian", 25, "Easy", 4.8,
         ["pasta", "parmesan", "cream", "garlic", "butter", "black pepper"],
         ["Boil pasta until al dente.", "Saute garlic in butter.", "Add cream and parmesan.", "Toss pasta through the sauce.", "Finish with black pepper."]),
        ("Margherita Pizza", "Classic pizza with tomato, mozzarella and fresh basil.", "Italian", 35, "Medium", 4.8,
         ["pizza dough", "tomato", "mozzarella", "basil", "olive oil"],
         ["Stretch the dough.", "Spread tomato sauce.", "Add mozzarella.", "Bake until the crust is golden.", "Finish with basil and olive oil."]),
        ("Pesto Pasta", "Fresh basil pesto with pasta, parmesan and toasted nuts.", "Italian", 20, "Easy", 4.6,
         ["pasta", "basil", "parmesan", "pine nuts", "garlic", "olive oil"],
         ["Blend basil, garlic, nuts and oil.", "Boil pasta.", "Toss hot pasta with pesto.", "Add parmesan.", "Serve immediately."]),
    ]),
    ("Mexican", "mexican", [
        ("Chicken Tacos", "Soft tortillas filled with juicy seasoned chicken and fresh salsa.", "Mexican", 25, "Easy", 4.7,
         ["chicken", "tortilla", "tomato", "onion", "lime", "coriander"],
         ["Season and cook chicken.", "Warm tortillas.", "Prepare tomato-onion salsa.", "Fill tortillas with chicken.", "Top with salsa and lime."]),
        ("Guacamole", "Creamy avocado dip with lime, tomato and coriander.", "Mexican", 10, "Easy", 4.5,
         ["avocado", "lime", "tomato", "onion", "coriander", "salt"],
         ["Mash ripe avocado.", "Fold in diced tomato and onion.", "Add lime and coriander.", "Season to taste.", "Serve chilled."]),
    ]),
    ("American", "american", [
        ("Classic Cheeseburger", "Juicy beef patty with cheddar, lettuce, tomato and a toasted bun.", "American", 25, "Medium", 4.7,
         ["beef", "burger bun", "cheddar", "lettuce", "tomato", "onion"],
         ["Shape and season the patty.", "Sear the patty on a hot pan.", "Add cheddar.", "Toast the bun.", "Assemble with vegetables and sauce."]),
        ("Pancake Stack", "Fluffy pancakes layered with berries and maple syrup.", "American", 20, "Easy", 4.6,
         ["flour", "milk", "egg", "butter", "maple syrup", "berries"],
         ["Whisk dry and wet ingredients separately.", "Combine gently.", "Cook pancakes on a greased pan.", "Stack pancakes.", "Top with berries and syrup."]),
    ]),
    ("Healthy", "healthy", [
        ("Greek Salad", "Crisp vegetables, feta and olives with a bright lemon dressing.", "Mediterranean", 15, "Easy", 4.8,
         ["cucumber", "tomato", "feta", "olive", "onion", "lemon"],
         ["Chop vegetables.", "Add feta and olives.", "Whisk lemon dressing.", "Toss everything together.", "Serve fresh."]),
        ("Grilled Chicken Salad", "Protein-rich grilled chicken over crunchy greens and vegetables.", "Healthy", 25, "Easy", 4.7,
         ["chicken", "lettuce", "cucumber", "tomato", "lemon", "olive oil"],
         ["Season chicken.", "Grill until cooked through.", "Slice vegetables.", "Combine greens and vegetables.", "Top with chicken and dressing."]),
    ]),
    ("Dessert", "dessert", [
        ("Chocolate Mug Cake", "A quick warm chocolate cake ready in minutes.", "Dessert", 8, "Easy", 4.5,
         ["flour", "cocoa", "sugar", "milk", "butter", "chocolate"],
         ["Mix dry ingredients in a mug.", "Add milk and melted butter.", "Stir until smooth.", "Microwave until just set.", "Rest briefly before serving."]),
    ]),
]

IMAGES = {
    "Chicken Biryani": "https://images.unsplash.com/photo-1563379091339-03246963d51a?auto=format&fit=crop&w=1000&q=80",
    "Paneer Tikka": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?auto=format&fit=crop&w=1000&q=80",
    "Vegetable Pulao": "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=1000&q=80",
    "Creamy Alfredo Pasta": "https://images.unsplash.com/photo-1645112411341-6c4fd023714a?auto=format&fit=crop&w=1000&q=80",
    "Margherita Pizza": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=1000&q=80",
    "Pesto Pasta": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=1000&q=80",
    "Chicken Tacos": "https://images.unsplash.com/photo-1552332386-f8dd00dc2f85?auto=format&fit=crop&w=1000&q=80",
    "Guacamole": "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1000&q=80",
    "Classic Cheeseburger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1000&q=80",
    "Pancake Stack": "https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=1000&q=80",
    "Greek Salad": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=1000&q=80",
    "Grilled Chicken Salad": "https://images.unsplash.com/photo-1546793665-c74683f339c1?auto=format&fit=crop&w=1000&q=80",
    "Chocolate Mug Cake": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=1000&q=80",
}

class Command(BaseCommand):
    help = "Create demo categories, meals and demo user."

    def handle(self, *args, **kwargs):
        Meal.objects.all().delete()
        Category.objects.all().delete()

        for category_name, slug, meals in DATA:
            category = Category.objects.create(name=category_name, slug=slug)
            for name, description, cuisine, time, difficulty, rating, ingredients, instructions in meals:
                Meal.objects.create(
                    name=name,
                    description=description,
                    category=category,
                    cuisine=cuisine,
                    image_url=IMAGES.get(name, ""),
                    cooking_time=time,
                    difficulty=difficulty,
                    rating=rating,
                    ingredients=ingredients,
                    instructions=instructions,
                )

        demo, created = User.objects.get_or_create(
            username="demo@mealfinder.local",
            defaults={"email": "demo@mealfinder.local", "first_name": "Demo User"},
        )
        demo.email = "demo@mealfinder.local"
        demo.first_name = "Demo User"
        demo.set_password("Demo@12345")
        demo.save()

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Meal.objects.count()} meals and {Category.objects.count()} categories."
        ))
        self.stdout.write(self.style.SUCCESS(
            "Demo login: demo@mealfinder.local / Demo@12345"
        ))
