from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(source='review_set', many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_rating(self, obj):
        return obj.review_set.aggregate(avg=Avg('stars'))['avg']


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_products_count(self, obj):
        return obj.product_set.count()