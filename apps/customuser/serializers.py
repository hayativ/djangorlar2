from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id", "username", "email", "phone", "birth_date",
            "first_name", "last_name",
        )
        read_only_fields = ("id",)


# class AdvancedUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AdvancedUser
#         fields = (
#             "id", "email", "first_name", "last_name",
#             "is_active", "date_joined",
#         )
#         read_only_fields = ("id", "date_joined")
