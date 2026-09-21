from django.contrib.auth.models import User
from django.db import models
from meals.models import Meal

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "meal"], name="unique_user_meal_favorite")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} → {self.meal}"
