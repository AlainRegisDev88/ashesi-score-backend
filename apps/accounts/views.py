from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # Only Super Admins should manage users
    filterset_fields = ['role', 'sport', 'is_active']