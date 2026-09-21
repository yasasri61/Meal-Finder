from django.contrib.auth.decorators import login_required
from django.urls import path
from django.shortcuts import get_object_or_404, redirect, render
from meals.models import Meal
from .models import Favorite

@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("meal", "meal__category")
    return render(request, "favorites/list.html", {"favorites": favorites})

@login_required
def toggle_favorite(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, meal=meal)
    if not created:
        favorite.delete()
    return redirect(request.POST.get("next") or request.META.get("HTTP_REFERER") or "meal_detail", pk=pk)

urlpatterns = [
    path("", favorites_view, name="favorites"),
    path("toggle/<int:pk>/", toggle_favorite, name="toggle_favorite"),
]
