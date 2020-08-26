from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MessageViewSet, RoomViewSet


router = DefaultRouter()
router.register(r'(?P<room>[0-9]+)/messages', MessageViewSet, basename='message')
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
]
