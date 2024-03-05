from django.urls import path
from .views import movie_list, movie_detail, director_list, movie_review_list

urlpatterns = [
    path('movies/', movie_list, name='movie-list'),
    path('movies/<int:pk>/', movie_detail, name='movie-detail'),
    path('directors/', director_list, name='director-list'),
    path('movies/reviews/', movie_review_list, name='movie-review-list'),

]
