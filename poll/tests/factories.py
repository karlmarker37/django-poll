from datetime import datetime

import factory

from poll.models import PollCampaign, PollOption, Poll


class PollCampaignFactory(factory.django.DjangoModelFactory):
    title_en = factory.Sequence(lambda n: f'Test Campaign {n}')
    title_zh = ''
    effective_from = datetime(2020, 1, 1).astimezone()
    effective_to = datetime(2021, 1, 1).astimezone()

    class Meta:
        model = PollCampaign


class PollOptionFactory(factory.django.DjangoModelFactory):
    campaign = factory.SubFactory(PollCampaignFactory)
    name_en = factory.Sequence(lambda n: f'Test option {n}')
    name_zh = ''

    class Meta:
        model = PollOption


class PollFactory(factory.django.DjangoModelFactory):
    option = factory.SubFactory(PollOptionFactory)
    user = factory.SubFactory('user.tests.factories.UserFactory')

    class Meta:
        model = Poll
