from rest_framework import serializers
from .models import Director, Movie, Review
from django.db.models import Avg

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.IntegerField(source='movies.count', read_only=True)
    class Meta:
        model = Director
        fields = 'name movies_count'.split()

class DirectorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'name'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text stars'.split()

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    director = serializers.PrimaryKeyRelatedField(source='director.name', read_only=True)
    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('stars'))['stars__avg']
    class Meta:
        model = Movie
        fields = 'title description duration director reviews rating'.split()

