from django.db import models

from applications.users.models import User
from applications.targets.models import Topic


class Room(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(User)

    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    content = models.CharField(max_length=250)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
