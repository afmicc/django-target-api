from rest_framework import permissions

from .models import Room


class IsRoomMember(permissions.BasePermission):
    def has_permission(self, request, view):
        room_id = view.kwargs['room']
        is_room_member = Room.objects.filter(
            id=room_id,
            members__id=request.user.id,
        ).exists()

        return is_room_member
