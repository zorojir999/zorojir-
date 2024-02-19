from django.contrib import admin

from movie_app.models import Movie, Review,Director

admin.site.register(Movie)
admin.site.register(Director)
admin.site.register(Review)
