from django.contrib import admin

from .models import Content


class ContentAdmin(admin.ModelAdmin):
    list_display = ('key', 'title', )
    search_fields = ('key', 'title', )


admin.site.register(Content, ContentAdmin)
