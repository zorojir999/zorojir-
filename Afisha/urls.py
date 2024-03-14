from django.contrib import admin
from django.urls import path
from movie_app.views import (
    MovieList,
    MovieDetail,
    DirectorList,
    DirectorDetail,
    MovieReviewList,
    MovieReviewDetail
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/movies/', MovieList.as_view(), name='movie-list'),
    path('api/v1/movies/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('api/v1/directors/', DirectorList.as_view(), name='director-list'),
    path('api/v1/directors/<int:pk>/', DirectorDetail.as_view(), name='director-detail'),
    path('api/v1/movie-reviews/', MovieReviewList.as_view(), name='movie-review-list'),
    path('api/v1/movie-reviews/<int:pk>/', MovieReviewDetail.as_view(), name='movie-review-detail'),
]
