from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from meals.models import Meal
from .models import Review

@login_required
def add_review(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == "POST":
        try:
            rating = int(request.POST.get("rating", 0))
        except ValueError:
            rating = 0
        comment = request.POST.get("comment", "").strip()
        if rating not in range(1, 6):
            messages.error(request, "Please choose a rating from 1 to 5.")
        elif not comment:
            messages.error(request, "Please write a short review.")
        else:
            Review.objects.update_or_create(
                user=request.user,
                meal=meal,
                defaults={"rating": rating, "comment": comment},
            )
            messages.success(request, "Your review was saved.")
    return redirect("meal_detail", pk=pk)

urlpatterns = [
    path("add/<int:pk>/", add_review, name="add_review"),
]
