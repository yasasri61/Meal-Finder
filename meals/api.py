from rest_framework import serializers, viewsets
from .models import Category, Meal

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class MealSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Meal
        fields = [
            "id", "name", "description", "category", "category_name", "cuisine",
            "image_url", "ingredients", "instructions", "cooking_time",
            "difficulty", "rating"
        ]

class MealViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MealSerializer

    def get_queryset(self):
        qs = Meal.objects.select_related("category").all()
        search = self.request.query_params.get("search", "").strip()
        category = self.request.query_params.get("category", "").strip()
        cuisine = self.request.query_params.get("cuisine", "").strip()
        max_time = self.request.query_params.get("max_time", "").strip()
        if search:
            from django.db.models import Q
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search) | Q(cuisine__icontains=search))
        if category:
            qs = qs.filter(category__name__iexact=category)
        if cuisine:
            qs = qs.filter(cuisine__iexact=cuisine)
        if max_time.isdigit():
            qs = qs.filter(cooking_time__lte=int(max_time))
        return qs

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
