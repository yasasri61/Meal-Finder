from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm
from favorites.models import Favorite
from reviews.models import Review

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to MealFinder!")
        return redirect("home")
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.cleaned_data["user"])
        messages.success(request, "Welcome back!")
        return redirect(request.GET.get("next") or "home")
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")

@login_required
def profile_view(request):
    context = {
        "favorites_count": Favorite.objects.filter(user=request.user).count(),
        "reviews_count": Review.objects.filter(user=request.user).count(),
    }
    return render(request, "accounts/profile.html", context)
