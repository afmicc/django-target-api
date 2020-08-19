from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from .models import Room


class RoomCreator:

    @transaction.atomic
    def create_from_target_match(self, target, *members):
        if self._exists_equal_room(target.topic, *members):
            return None

        room = Room.objects.create(topic=target.topic)

        self._validate_members(room, *members)

        room.members.add(*members)

    def _exists_equal_room(self, topic, *members):
        if not len(members) == 2:
            return False

        return Room.objects.filter(
            members__id__in=[m.id for m in members],
            topic=topic,
        ).exists()

    def _validate_members(self, room, *members):
        if len(members) != 2:
            raise ValidationError({'members': _('You must create a room with two members')})
