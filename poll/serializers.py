from django.contrib.auth import get_user_model
from rest_framework import serializers

from poll.models import PollCampaign, PollOption, Poll

User = get_user_model()


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = (
            'option',
            'user',
        )
        extra_kwargs = {
            'option': {'write_only': True},
            'user': {'write_only': True},
        }


class PollOptionSerializer(serializers.ModelSerializer):
    campaign = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=PollCampaign.objects.all(),
    )
    polls_count = serializers.IntegerField(read_only=True)
    polled_by_user = serializers.BooleanField(read_only=True)

    class Meta:
        model = PollOption
        fields = (
            'id',
            'campaign',
            'name_en',
            'name_zh',
            'polls_count',
            'polled_by_user',
        )


class PollCampaignSerializer(serializers.ModelSerializer):
    options = PollOptionSerializer(many=True, read_only=True)

    class Meta:
        model = PollCampaign
        fields = (
            'id',
            'title_en',
            'title_zh',
            'effective_from',
            'effective_to',
            'options',
        )
