from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from habit.views import HabitViewSet

app_name = "habit"
router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
] + router.urls
