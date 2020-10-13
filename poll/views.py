from django.db.models import Count, Prefetch, Exists, OuterRef, Q
from django.utils import timezone
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from poll.models import PollCampaign, PollOption, Poll
from poll.serializers import (
    PollCampaignSerializer,
    PollOptionSerializer,
    PollSerializer,
)
from poll.services import (
    validate_one_poll_per_user,
    validate_within_campaign_effective_date,
)


class PollCampaignViewSet(
        GenericViewSet,
        CreateModelMixin,
        ListModelMixin,
        RetrieveModelMixin,
):
    serializer_class = PollCampaignSerializer

    def get_queryset(self):
        user = self.request.user
        polls_by_user = Poll.objects.filter(option=OuterRef('id'), user=user)
        annotated_options = PollOption.objects.annotate(
            polls_count=Count('polls', distinct=True),
            polled_by_user=Exists(polls_by_user),
        ).order_by('-polls_count', 'create_date')
        prefetch_options = Prefetch('options', queryset=annotated_options)

        # retrieve query params
        condition = Q()
        now = timezone.now()
        if 'effective' in self.request.query_params:
            condition = condition & Q(
                effective_from__lte=now,
                effective_to__gt=now,
            )
        if 'ended' in self.request.query_params:
            condition = condition & Q(effective_to__lte=now)

        return PollCampaign.objects \
            .filter(condition) \
            .prefetch_related(prefetch_options) \
            .order_by('effective_from')


class PollOptionViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = PollOptionSerializer
    queryset = PollOption.objects.all()


class PollViewSet(GenericViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()

    def create(self, request, *args, **kwargs):
        now = timezone.now()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        option = serializer.validated_data['option']
        campaign = option.campaign
        validate_within_campaign_effective_date(campaign, now)
        validate_one_poll_per_user(campaign, request.user)
        serializer.save(user=request.user)
        return Response(status=201)
