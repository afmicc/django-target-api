from django.contrib import admin

from .models import Message, Room


class MessagesInline(admin.TabularInline):
    model = Message
    fields = ('writer', 'content', 'created_at', 'is_read', )
    readonly_fields = ('writer', 'content', 'created_at', 'is_read', )

    def has_add_permission(self, *args):
        return False


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'members_names', 'created_at', )
    fields = ('topic', 'members', 'created_at', )
    filter_horizontal = ('members', )
    readonly_fields = ('created_at', )
    inlines = (MessagesInline, )

    def members_names(self, obj):
        members = obj.members.all()
        return f"'{members.first()}' and '{members.last()}'"

    members_names.short_description = 'members'


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'writer', 'content', 'created_at', 'is_read', )


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
