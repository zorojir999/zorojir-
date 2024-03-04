from django.db.models import Avg, Count
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer, ReviewSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        queryset = Movie.objects.all()
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=204)



@api_view(['GET', 'POST'])
def director_list(request):
    if request.method == 'GET':
        queryset = Director.objects.annotate(movies_count=Count('movie'))
        for director in queryset:
            director.movies_count = Movie.objects.filter(director_id=director.pk).count()
        serializer = DirectorSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
    elif request.method == 'POST':
        serializer = DirectorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail(request, id):
    director = get_object_or_404(Director, id=id)
    if request.method == 'GET':
        serializer = DirectorSerializer(director)
        return Response(serializer.data, status=200)
    elif request.method == 'PUT':
        serializer = DirectorSerializer(director, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    elif request.method == 'DELETE':
        director.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def movie_review_list(request):
    if request.method == 'GET':
        queryset = Movie.objects.prefetch_related('review_set')
        for movie in queryset:
            movie.avg_rating = movie.review_set.aggregate(Avg('stars'))['stars__avg']
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_review_detail(request, id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=200)
    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=204)

