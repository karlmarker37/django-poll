from django.test import TestCase
from django.utils import timezone

from poll.serializers import PollCampaignSerializer, PollOptionSerializer, PollSerializer
from poll.tests.factories import PollCampaignFactory, PollOptionFactory
from user.tests.factories import UserFactory


class TestPollSerializer(TestCase):
    def test_poll_serializer(self):
        # write
        option = PollOptionFactory.create()
        user = UserFactory.create()
        data = {
            'option': str(option.id),
            'user': str(user.id),
        }

        serializer = PollSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        poll = serializer.save()
        self.assertEqual(poll.option, option)
        self.assertEqual(poll.user, user)

        # no read
        data = PollSerializer(poll).data
        self.assertEqual(data, {})

    def test_poll_option_serializer(self):
        # write
        campaign = PollCampaignFactory.create()
        data = {
            'campaign': str(campaign.id),
            'name_en': 'foo',
            'name_zh': 'bar',
        }
        serializer = PollOptionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        option = serializer.save()

        self.assertEqual(option.campaign, campaign)
        self.assertEqual(option.name_en, 'foo')
        self.assertEqual(option.name_zh, 'bar')

        # read
        another_option = PollOptionFactory.create()
        options = [option, another_option]
        data = PollOptionSerializer(options, many=True).data
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], str(option.id))
        self.assertEqual(data[1]['id'], str(another_option.id))
        for d in data:
            self.assertCountEqual(
                d.keys(),
                {
                    'id',
                    'name_en',
                    'name_zh',
                }
            )

    def test_poll_campaign_serializer(self):
        # write
        now = timezone.now()
        data = {
            'title_en': 'foo',
            'title_zh': 'bar',
            'effective_from': now.isoformat(),
            'effective_to': now.isoformat(),
        }
        serializer = PollCampaignSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        campaign = serializer.save()

        self.assertEqual(campaign.title_en, 'foo')
        self.assertEqual(campaign.title_zh, 'bar')
        self.assertEqual(campaign.effective_from, now)
        self.assertEqual(campaign.effective_to, now)

        # read
        another_campaign = PollCampaignFactory.create()
        campaigns = [campaign, another_campaign]
        data = PollCampaignSerializer(campaigns, many=True).data
        self.assertEqual(len(data), 2)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], str(campaign.id))
        self.assertEqual(data[1]['id'], str(another_campaign.id))
        for d in data:
            self.assertCountEqual(
                d.keys(),
                {
                    'id',
                    'title_en',
                    'title_zh',
                    'effective_from',
                    'effective_to',
                    'options',
                }
            )
