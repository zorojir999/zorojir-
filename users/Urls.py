from django.urls import path
from . import views
urlpatterns = [
    path('users/registration/', views.registration_api_view),
    path('users/confirm/', views.confirm_user_api_view),
    path('users/authorization/', views.authorization_api_view),
    path('users/logout/', views.logout),
]
