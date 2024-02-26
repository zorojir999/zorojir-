
from rest_framework import generics
from django.db.models import Avg, Count, OuterRef
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer

class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieDetail(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieReviewList(generics.ListAPIView):
    queryset = Movie.objects.prefetch_related('review_set')
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        for movie in queryset:
            movie.avg_rating = movie.review_set.aggregate(Avg('stars'))['stars__avg']
        return queryset

class DirectorList(generics.ListAPIView):
    queryset = Director.objects.annotate(movies_count=Count('movie'))
    serializer_class = DirectorSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['movies_count'] = Movie.objects.filter(director_id=OuterRef('pk')).count()
        return context
