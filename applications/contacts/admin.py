from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'writer', 'short_message', 'created_at',)
    list_filter = ('created_at',)
    search_fields = ('email', 'message',)
    fields = ('email', 'writer', 'message', 'created_at', 'updated_at',)

    def short_message(self, obj):
        return f'{obj.message[:60]}...' if len(obj.message) > 60 else obj.message

    short_message.short_description = 'message'

    def has_add_permission(self, *args):
        return False

    def has_change_permission(self, *args):
        return False


admin.site.register(Contact, ContactAdmin)
