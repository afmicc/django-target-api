from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from applications.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        FEMALE = 'F', _('Female')
        MALE = 'M', _('Male')
        OTHER = 'O', _('Other')

    username = None
    email = models.EmailField(_('email address'), unique=True)
    gender = models.CharField(choices=Gender.choices, default=Gender.OTHER, max_length=10)
    name = models.CharField(blank=True, max_length=250)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    picture = models.ImageField(upload_to='users/pictures', blank=True, null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.name
