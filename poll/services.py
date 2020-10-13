from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from poll.models import PollCampaign

User = get_user_model()


def validate_within_campaign_effective_date(
        campaign: PollCampaign,
        poll_date: datetime,
) -> True:
    if campaign.effective_from <= poll_date < campaign.effective_to:
        return True
    raise ValidationError(f'Polls are only allowed from'
                          f' {campaign.effective_from} to'
                          f' {campaign.effective_to}.')


def validate_one_poll_per_user(
        campaign: PollCampaign,
        user: User,
) -> True:
    if campaign.options.filter(polls__user=user).exists():
        raise ValidationError(f'Allow polling once per campaign only.')
    return True
