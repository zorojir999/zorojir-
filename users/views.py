from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from Afisha import settings
from .models import UserConfirmation
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserConfirmationSerializer
import random

class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        code = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        confirmation = UserConfirmation.objects.create(user=user, code=code)
        confirmation.save()

        send_mail('Verification Code', f'Your verification code is: {code}', settings.EMAIL_HOST_USER, [user.email])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ConfirmUserAPIView(APIView):
    def post(self, request):
        serializer = UserConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')

        try:
            confirmation = UserConfirmation.objects.get(code=code)
        except UserConfirmation.DoesNotExist:
            return Response({'error': 'Invalid confirmation code'}, status=status.HTTP_404_NOT_FOUND)

        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()

        return Response({'status': 'User activated'}, status=status.HTTP_200_OK)

class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def get(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            logout(request)
            return Response({'message': 'User logged out'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'message': 'User is already logged out'}, status=status.HTTP_200_OK)
