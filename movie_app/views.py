from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializers import (DirectorSerializer, MovieSerializer, ReviewSerializer, MovieDetailSerializer,
                          MovieValidateSerializer, ReviewValidateSerializer, DirectorValidateSerializer)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

class DirectorListAPIView(ListCreateAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    pagination_class = CustomPagination

    def post(request):
        if request.method == 'POST':
            serializer = DirectorValidateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data=serializer.errors)

            name = serializer.validated_data.get('name')
            director = Director(name=name)
            director.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=DirectorSerializer(director).data)



class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorSerializer
    queryset = Director.objects.all()
    pagination_class = CustomPagination
    def put(request, id):
        try:
            director = Director.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response(data={'error': 'Director not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'PUT':
            serializer = DirectorValidateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            director.name = serializer.validated_data.get('name')
            director.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=DirectorSerializer(director).data)





class ReviewViewSet(ModelViewSet):
    serializer_class = DirectorSerializer
    queryset = Review.objects.all()
    pagination_class = CustomPagination
    def put(request, id):
        try:
            review = Review.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response(data={'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'PUT':
            serializer = ReviewValidateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data=serializer.errors)

            review.text = serializer.validated_data.get('text')
            review.stars = serializer.validated_data.get('stars')
            review.movie_id = serializer.validated_data.get('movie_id')
            review.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=ReviewSerializer(review).data)

    def post(request):
        if request.method == 'POST':
            serializer = ReviewValidateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data=serializer.errors)

            text = serializer.validated_data.get('text')
            stars = serializer.validated_data.get('stars')
            movie_id = serializer.validated_data.get('movie_id')
            review = Review(
                text=text,
                stars=stars,
                movie_id=movie_id
            )
            review.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=ReviewSerializer(review).data)

class MovieViewSet(ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    pagination_class = CustomPagination
    def put(request, id):
        try:
            movie = Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response(data={'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'PUT':
            serializer = MovieValidateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            movie.title = serializer.validated_data.get('title')
            movie.description = serializer.validated_data.get('description')
            movie.duration = serializer.validated_data.get('duration')
            movie.director_id = serializer.validated_data.get('director_id')
            movie.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=MovieDetailSerializer(movie).data)

    def post(request):
        if request.method == 'POST':
            serializer = MovieValidateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data=serializer.errors)

            title = serializer.validated_data.get('title')
            description = serializer.validated_data.get('description')
            duration = serializer.validated_data.get('duration')
            director_id = serializer.validated_data.get('director_id')
            movie = Movie(
                title=title,
                description=description,
                duration=duration,
                director_id=director_id
            )
            movie.save()
            return Response(status=status.HTTP_201_CREATED,
                            data=MovieDetailSerializer(movie).data)

