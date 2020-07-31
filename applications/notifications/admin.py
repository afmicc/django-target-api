from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'message', 'created_at',)
    list_filter = ('created_at',)

    def has_add_permission(self, *args):
        return False

    def has_change_permission(self, *args):
        return False

    def has_delete_permission(self, *args):
        return False


admin.site.register(Notification, NotificationAdmin)
