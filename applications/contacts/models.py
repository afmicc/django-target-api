from django.db import models

from applications.users.models import User


class Contact(models.Model):
    email = models.EmailField(blank=False, null=False)
    message = models.TextField(max_length=500, blank=False, null=False)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-created_at']
