from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Director, Movie, Review

def validate_text_min_length(value, min_length):
    if len(value) < min_length:
        raise ValidationError(f'Минимальная длина для этого поля должна быть {min_length}')
    return value

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_text(self, value):
        return validate_text_min_length(value, 5)
