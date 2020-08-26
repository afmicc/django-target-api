from rest_framework import serializers

from .models import Message, Room
from applications.users.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('content', 'room', 'writer', 'created_at', )

    room = serializers.ReadOnlyField(source='room.id')
    writer = serializers.ReadOnlyField(source='writer.name')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'created_at', 'topic', 'receiver', )
        read_only_fields = ('id', 'created_at', 'topic', 'receiver', )

    topic = serializers.ReadOnlyField(source='topic.name')
    receiver = serializers.SerializerMethodField()

    def get_receiver(self, obj):
        current_user = self.context['request'].user
        receiver = obj.members.exclude(id=current_user.id).first()
        return UserSerializer(receiver).data
