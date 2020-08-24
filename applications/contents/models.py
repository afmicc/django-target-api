from django.db import models


class Content(models.Model):
    key = models.CharField(max_length=20, default='', unique=True)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
