from datetime import datetime

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from poll.services import validate_one_poll_per_user, validate_within_campaign_effective_date
from poll.tests.factories import PollCampaignFactory, PollOptionFactory, PollFactory
from user.tests.factories import UserFactory


class PollServiceTest(TestCase):
    def test_validate_within_campaign_effective_date(self):
        campaign = PollCampaignFactory.create()
        now = datetime(2020, 2, 29).astimezone()

        self.assertTrue(validate_within_campaign_effective_date(campaign, now))

        campaign.effective_from = datetime(2020, 2, 29, 0, 0, 1).astimezone()
        campaign.save()
        with self.assertRaises(ValidationError):
            validate_within_campaign_effective_date(campaign, now)

        campaign.effective_from = datetime(2020, 2, 29, 0, 0, 0).astimezone()
        campaign.effective_to = datetime(2020, 2, 29, 0, 0, 0).astimezone()
        campaign.save()
        with self.assertRaises(ValidationError):
            validate_within_campaign_effective_date(campaign, now)

    def test_validate_one_poll_per_user(self):
        campaign = PollCampaignFactory.create()
        user = UserFactory.create()
        self.assertTrue(validate_one_poll_per_user(campaign, user))

        option = PollOptionFactory.create(campaign=campaign)
        PollFactory.create(option=option, user=user)
        with self.assertRaises(ValidationError):
            validate_one_poll_per_user(campaign, user)
