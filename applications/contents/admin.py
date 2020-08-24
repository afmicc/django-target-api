from django import forms
from django.contrib import admin

from .models import Content


class ContentModelForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Content
        fields = '__all__'


class ContentAdmin(admin.ModelAdmin):
    form = ContentModelForm
    list_display = ('key', 'title', )
    search_fields = ('key', 'title', )


admin.site.register(Content, ContentAdmin)
