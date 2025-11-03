from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdvancedUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("phone", "birth_date")}),
    )


@admin.register(AdvancedUser)
class AdvancedUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_active", "is_staff")
