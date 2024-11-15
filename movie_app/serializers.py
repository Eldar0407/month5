from rest_framework import serializers
from .models import Director, Movie, Review
from django.db.models import Avg
from rest_framework.exceptions import ValidationError

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

class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=100)
    description = serializers.CharField(required=False)
    duration = serializers.IntegerField(required=True)
    director_id = serializers.IntegerField(min_value=1)

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except:
            raise ValidationError('Director does not exist!')
        return director_id

class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=1, max_length=50)

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField()
    movie_id = serializers.IntegerField(min_value=1)
    stars = serializers.IntegerField(min_value=1, max_value=5)

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except:
            raise ValidationError('Director does not exist!')
        return movie_id