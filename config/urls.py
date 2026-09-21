from django.contrib import admin
from django.urls import include, path
from meals.api import MealViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("meals", MealViewSet, basename="api-meals")
router.register("categories", CategoryViewSet, basename="api-categories")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("meals.urls")),
    path("accounts/", include("accounts.urls")),
    path("favorites/", include("favorites.urls")),
    path("reviews/", include("reviews.urls")),
    path("api/", include(router.urls)),
]
