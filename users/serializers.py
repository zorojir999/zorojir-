# serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('Аккаунт не активирован. Проверьте вашу почту.')
            else:
                raise serializers.ValidationError('Неверное имя пользователя или пароль.')
        else:
            raise serializers.ValidationError('Укажите имя пользователя и пароль.')

        return data
