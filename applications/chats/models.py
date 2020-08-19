from django.db import models

from applications.users.models import User
from applications.targets.models import Topic


class Room(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(User)

    created_at = models.DateTimeField(auto_now_add=True)
