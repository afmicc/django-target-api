from rest_framework import mixins, permissions, viewsets

from .permissions import IsRoomMember
from .serializers import MessageSerializer, RoomSerializer


class RoomViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.room_set.all()


class MessageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsRoomMember]

    def get_queryset(self):
        room_id = self.kwargs['room']
        return self.request.user.room_set.get(id=room_id).message_set.all()
