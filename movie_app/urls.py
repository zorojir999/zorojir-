# urls.py
from django.urls import path
from .views import MovieList, MovieDetail, DirectorList, MovieReviewList

urlpatterns = [
    path('api/v1/movies/', MovieList.as_view(), name='movie-list'),
    path('api/v1/movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('api/v1/directors/', DirectorList.as_view(), name='director-list'),
    path('api/v1/movies/reviews/', MovieReviewList.as_view(), name='movie-review-list'),
]
