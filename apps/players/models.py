import uuid as uuid_lib

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import PlayerManager


class Player(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=30, unique=True)
    uuid = models.UUIDField(
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False,
        primary_key=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = PlayerManager()

    def __str__(self):
        return self.email
