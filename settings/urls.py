# Django modules
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from apps.tasks import views
from apps.tasks.views import hello_view
from apps.customuser.views import CustomUserViewSet, AdvancedUserViewSet

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='customuser')
router.register(r'advanced-users', AdvancedUserViewSet, basename='advanceduser')

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", views.welcome, name="welcome"),
    path("users/", views.users, name="users"),
    path("city-time/", views.city_time, name="city_time"),
    path("cnt/", views.counter, name="counter"),
    path("api/", include(router.urls)),
]
