from datetime import datetime
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from poll.models import PollCampaign, PollOption, Poll
from poll.tests.factories import (
    PollCampaignFactory,
    PollFactory,
    PollOptionFactory,
)
from user.tests.factories import UserFactory


class TestPollCampaignViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.test_campaigns = PollCampaignFactory.create_batch(size=2)
        cls.options = PollOptionFactory.create_batch(
            size=3,
            campaign=cls.test_campaigns[0],
        )
        PollFactory.create(option=cls.options[0], user=cls.user)

    def test_create_campaign(self):
        self.client.force_authenticate(self.user)
        view_name = 'v1:poll-campaign-list'

        effective_from = datetime(2020, 1, 1).astimezone()
        effective_to = datetime(2021, 1, 1).astimezone()
        payload = {
            'title_en': 'foo',
            'title_zh': '',
            'effective_from': effective_from.isoformat(),
            'effective_to': effective_to.isoformat(),
        }
        campaign_count = PollCampaign.objects.count()
        response = self.client.post(reverse(view_name), data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PollCampaign.objects.count(), campaign_count + 1)
        new_campaign = PollCampaign.objects.order_by('-create_date').first()
        self.assertEqual(new_campaign.title_en, 'foo')
        self.assertEqual(new_campaign.title_zh, '')
        self.assertEqual(new_campaign.effective_from, effective_from)
        self.assertEqual(new_campaign.effective_to, effective_to)

    def test_list_campaign(self):
        self.client.force_authenticate(self.user)
        view_name = 'v1:poll-campaign-list'

        response = self.client.get(reverse(view_name))

        data = response.data[2:]  # 2 in migrations
        self.assertEqual(len(data), 2)
        for i, d in enumerate(data):
            self.assertEqual(d['id'], str(self.test_campaigns[i].id))
            self.assertEqual(d['title_en'], self.test_campaigns[i].title_en)
            self.assertEqual(d['title_zh'], self.test_campaigns[i].title_zh)
            effective_from = self.test_campaigns[i].effective_from.isoformat()
            effective_to = self.test_campaigns[i].effective_to.isoformat()
            self.assertEqual(d['effective_from'], effective_from)
            self.assertEqual(d['effective_to'], effective_to)

        self.assertEqual(len(data[0]['options']), len(self.options))
        for option_data, option in zip(data[0]['options'], self.options):
            self.assertEqual(option_data['id'], str(option.id))
            self.assertEqual(option_data['name_en'], option.name_en)
            self.assertEqual(option_data['name_zh'], option.name_zh)
        self.assertEqual(data[0]['options'][0]['polls_count'], 1)
        self.assertEqual(data[0]['options'][0]['polled_by_user'], True)
        self.assertEqual(data[0]['options'][1]['polls_count'], 0)
        self.assertEqual(data[0]['options'][1]['polled_by_user'], False)
        self.assertEqual(data[0]['options'][2]['polls_count'], 0)
        self.assertEqual(data[0]['options'][2]['polled_by_user'], False)

        # query param `effective`
        response = self.client.get(reverse(view_name), data={'effective': 1})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], str(self.test_campaigns[0].id))
        self.assertEqual(response.data[1]['id'], str(self.test_campaigns[1].id))

        # query param `ended`
        response = self.client.get(reverse(view_name), data={'ended': 1})
        ended_campaigns = PollCampaign.objects.filter(
            effective_to__lte=timezone.now(),
        )
        self.assertEqual(len(response.data), ended_campaigns.count())
        self.assertEqual(response.data[0]['id'], str(ended_campaigns[0].id))
        self.assertEqual(response.data[1]['id'], str(ended_campaigns[1].id))

        # `effective` + `ended` is contradictory
        response = self.client.get(reverse(view_name), data={
            'effective': 1,
            'ended': 1,
        })
        self.assertEqual(len(response.data), 0)

    def test_retrieve_campaign(self):
        self.client.force_authenticate(self.user)
        view_name = 'v1:poll-campaign-detail'
        pk = str(self.test_campaigns[0].id)
        response = self.client.get(reverse(view_name, kwargs={'pk': pk}))
        self.assertEqual(response.data['id'], pk)


class TestPollOptionViewSet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.campaign = PollCampaignFactory.create()

    def test_create_option(self):
        self.client.force_authenticate(self.user)
        view_name = 'v1:poll-option-list'
        payload = {
            'campaign': str(self.campaign.id),
            'name_en': 'Test create option',
            'name_zh': '',
        }
        option_count = PollOption.objects.count()

        response = self.client.post(reverse(view_name), data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PollOption.objects.count(), option_count + 1)
        option = PollOption.objects.order_by('-create_date').first()
        self.assertEqual(option.campaign, self.campaign)
        self.assertEqual(option.name_en, 'Test create option')
        self.assertEqual(option.name_zh, '')


class TestPollViewSet(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.option = PollOptionFactory.create()

    @patch('poll.views.validate_one_poll_per_user', autospec=True)
    @patch('poll.views.validate_within_campaign_effective_date', autospec=True)
    @patch('poll.views.timezone.now', return_value=timezone.now())
    def test_create_poll(
            self,
            mock_now,
            mock_validate_within_campaign_effective_date,
            mock_validate_one_poll_per_user,
    ):
        self.client.force_authenticate(self.user)
        view_name = 'v1:poll-list'
        payload = {
            'option': str(self.option.id),
            'user': str(self.user.id),
        }
        poll_count = Poll.objects.count()

        response = self.client.post(reverse(view_name), data=payload)
        mock_validate_within_campaign_effective_date.assert_called_once_with(
            self.option.campaign,
            mock_now.return_value,
        )
        mock_validate_one_poll_per_user.assert_called_once_with(
            self.option.campaign,
            self.user,
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Poll.objects.count(), poll_count + 1)
        poll = Poll.objects.order_by('-create_date').first()
        self.assertEqual(poll.option, self.option)
        self.assertEqual(poll.user, self.user)
