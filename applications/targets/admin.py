from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from datetime import timedelta
from django.utils import timezone

from applications.targets.models import Target, Topic


class TargetAdmin(OSMGeoAdmin):
    fields = ('title', 'owner', 'topic', 'location', 'radius', 'created_at', )
    readonly_fields = ('created_at', )
    list_display = ('title', 'owner', 'topic', 'location', 'radius', 'created_at', )
    search_fields = ('title', 'topic', )

    def has_delete_permission(self, request, target=None):
        return (
            request.user.is_superuser and
            target and
            target.created_at < (timezone.now() - timedelta(days=7))
        )


admin.site.register(Target, TargetAdmin)
admin.site.register(Topic)
