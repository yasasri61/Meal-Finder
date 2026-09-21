from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("meal", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("meal__name", "user__username", "comment")
