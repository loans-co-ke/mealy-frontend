from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RegisterViewSet, LoginViewSet, RefreshTokenViewSet

urlpatterns = [
    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', LoginViewSet.as_view({'post': 'create'}), name='login'),
    path('refresh_token/', RefreshTokenViewSet.as_view({'post': 'create'}), name='refresh_token'),
]