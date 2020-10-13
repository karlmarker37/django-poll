from django.urls import include, path

from poll_api.routers import OptionalTrailingSlashRouter
from user.views import UserViewSet

user_router = OptionalTrailingSlashRouter()

user_router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(user_router.urls)),
]
