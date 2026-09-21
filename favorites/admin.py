from django.contrib import admin
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "meal", "created_at")
    search_fields = ("user__username", "meal__name")
