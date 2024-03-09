from django.urls import path
from .views import MovieList, MovieDetail, DirectorList, MovieReviewList

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movie-list'),
    path('movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('directors/', DirectorList.as_view(), name='director-list'),
    path('movies/reviews/', MovieReviewList.as_view(), name='movie-review-list'),
]

