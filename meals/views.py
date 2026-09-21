from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Category, Meal
from favorites.models import Favorite
from reviews.models import Review

def home(request):
    featured = Meal.objects.all()[:8]
    categories = Category.objects.all()
    return render(request, "home.html", {"featured": featured, "categories": categories})

def meal_list(request):
    meals = Meal.objects.select_related("category").all()
    search = request.GET.get("search", "").strip()
    category = request.GET.get("category", "").strip()
    cuisine = request.GET.get("cuisine", "").strip()
    max_time = request.GET.get("max_time", "").strip()
    difficulty = request.GET.get("difficulty", "").strip()

    if search:
        meals = meals.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(cuisine__icontains=search)
        )
    if category:
        meals = meals.filter(category__name__iexact=category)
    if cuisine:
        meals = meals.filter(cuisine__iexact=cuisine)
    if max_time and max_time.isdigit():
        meals = meals.filter(cooking_time__lte=int(max_time))
    if difficulty:
        meals = meals.filter(difficulty__iexact=difficulty)

    paginator = Paginator(meals, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "cuisines": Meal.objects.values_list("cuisine", flat=True).distinct().order_by("cuisine"),
        "search": search,
        "selected_category": category,
        "selected_cuisine": cuisine,
        "selected_max_time": max_time,
        "selected_difficulty": difficulty,
    }
    return render(request, "meals/list.html", context)

def meal_detail(request, pk):
    meal = get_object_or_404(Meal.objects.select_related("category"), pk=pk)
    request.session["recently_viewed"] = [pk] + [x for x in request.session.get("recently_viewed", []) if x != pk]
    request.session["recently_viewed"] = request.session["recently_viewed"][:6]
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(user=request.user, meal=meal).exists()
    reviews = Review.objects.filter(meal=meal).select_related("user")
    return render(request, "meals/detail.html", {"meal": meal, "is_favorite": is_favorite, "reviews": reviews})

def ingredient_finder(request):
    query = request.GET.get("ingredients", "").strip()
    results = []
    ingredients = [x.strip().lower() for x in query.split(",") if x.strip()]
    if ingredients:
        for meal in Meal.objects.all():
            meal_ingredients = [str(x).lower() for x in meal.ingredients]
            matches = [x for x in ingredients if any(x in item for item in meal_ingredients)]
            score = round((len(set(matches)) / max(len(meal_ingredients), 1)) * 100)
            if matches:
                results.append({"meal": meal, "matches": matches, "score": score})
        results.sort(key=lambda item: (-item["score"], -float(item["meal"].rating)))
    return render(request, "meals/ingredient_finder.html", {"results": results, "query": query})
