from django.contrib.auth import get_user_model
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet

from user.serializers import UserSerializer

User = get_user_model()


class UserViewSet(GenericViewSet):
    permission_classes = []
    authentication_classes = []
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.pop('password')
        user = serializer.save()
        user.set_password(password)
        user.save()
        return Response(status=201)
