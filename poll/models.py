import uuid

from django.db import models
from django.utils import timezone


class PollCampaign(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title_en = models.TextField()
    title_zh = models.TextField(blank=True)
    effective_from = models.DateTimeField()
    effective_to = models.DateTimeField()
    create_date = models.DateTimeField(default=timezone.now, editable=False)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('create_date',)


class PollOption(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    campaign = models.ForeignKey(
        PollCampaign,
        related_name='options',
        on_delete=models.PROTECT,
    )
    name_en = models.TextField()
    name_zh = models.TextField(blank=True)
    create_date = models.DateTimeField(default=timezone.now, editable=False)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('create_date',)


class Poll(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        'user.User',
        related_name='polls',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    option = models.ForeignKey(
        PollOption,
        related_name='polls',
        on_delete=models.PROTECT,
    )
    create_date = models.DateTimeField(default=timezone.now, editable=False)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('create_date',)
