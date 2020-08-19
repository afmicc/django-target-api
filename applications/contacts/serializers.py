from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ('id', 'created_at', 'updated_at',)

    writer = serializers.ReadOnlyField(source='writer.id', required=False, allow_null=True)
