from rest_framework import status, mixins, permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer, LoginSerializer, RefreshTokenSerializer
from .models import User

class RegisterViewSet(ModelViewSet):
    http_method_names = ['post']

    serializer_class = RegistrationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        user.is_verified = True
        user.save()

        return Response(user_data, status=status.HTTP_201_CREATED)
    
class LoginViewSet(ModelViewSet):
    http_method_names = ['post']

    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class RefreshTokenViewSet(ModelViewSet):

    http_method_names = ['post']
    serializer_class = RefreshTokenSerializer

    def create(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh_token']
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)

            return Response({
                'refresh_token': refresh_token,
                'access_token': access_token
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)