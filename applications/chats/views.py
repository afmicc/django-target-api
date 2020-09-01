from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=True, methods=['post'])
    def set_last_message_read(self, request, **args):
        message = self.get_object()
        unread_messages = (
            self.get_queryset()
            .filter(is_read=False, id__lte=message.id)
            .exclude(writer__id=self.request.user.id)
        )
        unread_messages.update(is_read=True)

        return Response(status=status.HTTP_204_NO_CONTENT)
