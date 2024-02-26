
from rest_framework import generics
from django.db.models import Avg, Count, OuterRef
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Avg, Count, OuterRef

@api_view(['GET'])
def movie_list(request):
    queryset = Movie.objects.all()
    serializer = MovieSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MovieSerializer(movie)
    return Response(serializer.data)

@api_view(['GET'])
def movie_review_list(request):
    queryset = Movie.objects.prefetch_related('review_set')
    for movie in queryset:
        movie.avg_rating = movie.review_set.aggregate(Avg('stars'))['stars__avg']
    serializer = MovieSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def director_list(request):
    queryset = Director.objects.annotate(movies_count=Count('movie'))
    for director in queryset:
        director.movies_count = Movie.objects.filter(director_id=director.pk).count()
    serializer = DirectorSerializer(queryset, many=True)
    return Response(serializer.data)
