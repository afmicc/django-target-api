from rest_framework import serializers

from .models import Message, Room
from applications.users.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    room = serializers.ReadOnlyField(source='room.id')
    writer = serializers.ReadOnlyField(source='writer.name')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ('members', )
        read_only_fields = ('id', 'created_at', 'topic', 'receiver', 'unread_message_count', )

    topic = serializers.ReadOnlyField(source='topic.name')
    receiver = serializers.SerializerMethodField()
    unread_message_count = serializers.SerializerMethodField()

    def get_receiver(self, obj):
        current_user = self.context['request'].user
        receiver = obj.members.exclude(id=current_user.id).first()
        return UserSerializer(receiver).data

    def get_unread_message_count(self, room):
        current_user = self.context['request'].user
        return (room.message_set.filter(is_read=False)
                                .exclude(writer__id=current_user.id)
                                .count())
