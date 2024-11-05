from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Director, Movie, Review
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer




@api_view(['GET'])
def DirectorDetailView(request, id):
    directors = Director.objects.get(id=id)
    data = DirectorSerializer(directors).data
    return Response(data=data)



@api_view(['GET'])
def DirectorView(request):
    directors = Director.objects.all()
    data = DirectorSerializer(directors, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def MovieDetailView(request, id):
    movies = Movie.objects.get(id=id)
    data = MovieSerializer(movies).data
    return Response(data=data)


@api_view(['GET'])
def MovieView(request):
    movies = Movie.objects.all()
    data = MovieSerializer(instance=movies, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def ReviewDetailView(request, id):
    reviews = Review.objects.get(id=id)
    data = ReviewSerializer(reviews).data
    return Response(data=data)

@api_view(['GET'])
def ReviewView(request):
    reviews = Review.objects.all()
    data = ReviewSerializer(instance=reviews, many=True).data
    return Response(data=data, status=status.HTTP_200_OK)




@api_view(['GET'])
def test_api_view(request):
    dict_ = {
        'str': 'Hello World!',
        'int': 100,
        'float': 2.77,
        'bool': True,
        'list': [1, 2, 3],
        'dict': {'key': 'value'}
    }
    return Response(data=[dict_])