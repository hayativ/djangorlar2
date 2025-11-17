from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser 

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("phone", "birth_date")}), 
    )
    list_display = UserAdmin.list_display + ("phone", "birth_date")
