from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]


# class AdvancedUserViewSet(viewsets.ModelViewSet):
#     queryset = AdvancedUser.objects.all()
#     serializer_class = AdvancedUserSerializer
#     permission_classes = [permissions.IsAdminUser]
