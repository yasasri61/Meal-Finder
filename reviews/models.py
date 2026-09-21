from django.contrib.auth.models import User
from django.db import models
from meals.models import Meal

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.meal} - {self.rating}/5"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not 1 <= self.rating <= 5:
            raise ValidationError("Rating must be between 1 and 5.")
