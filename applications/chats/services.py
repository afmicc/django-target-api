from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from .models import Room


class RoomCreator:

    @transaction.atomic
    def create_from_target_match(self, target, *members):
        if self._exists_equal_room(target.topic, *members):
            return

        self._validate_members(*members)
        room = Room.objects.create(topic=target.topic)
        room.members.add(*members)

    def _exists_equal_room(self, topic, *members):
        return (
            len(members) == 2 and
            Room.objects.filter(topic=topic)
                .filter(members__id=members[0].id)
                .filter(members__id=members[1].id)
                .exists()
        )

    def _validate_members(self, *members):
        if len(members) != 2:
            raise ValidationError({'members': _('You must create a room with two members')})
