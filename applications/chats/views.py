from rest_framework import mixins, permissions, viewsets

from .serializers import RoomSerializer


class RoomViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.room_set.all()
