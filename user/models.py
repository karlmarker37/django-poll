import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    identity_document_number = models.TextField()
    create_date = models.DateTimeField(default=timezone.now, editable=False)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ('create_date',)
