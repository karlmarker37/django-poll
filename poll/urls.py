from django.urls import include, path

from poll.views import PollCampaignViewSet, PollOptionViewSet, PollViewSet
from poll_api.routers import OptionalTrailingSlashRouter

poll_router = OptionalTrailingSlashRouter()

poll_router.register('poll/campaign', PollCampaignViewSet, basename='poll-campaign')  # noqa: B950
poll_router.register('poll/option', PollOptionViewSet, basename='poll-option')
poll_router.register('poll', PollViewSet, basename='poll')

urlpatterns = [
    path('', include(poll_router.urls)),
]
