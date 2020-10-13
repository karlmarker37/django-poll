from django.test import TestCase
from rest_framework.exceptions import ValidationError

from user.serializers import UserSerializer


class TestUserSerializer(TestCase):
    def test_user_serializer(self):
        # write
        data = {
            'username': 'foo',
            'password': 'bar',
            'identity_document_number': 'B875013(6)',
        }
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.assertEqual(user.username, 'foo')
        self.assertEqual(user.identity_document_number, 'B875013(6)')

        # duplicated username
        data = {
            'username': 'foo',
            'password': 'baz',
            'identity_document_number': 'B875013(6)',
        }
        serializer = UserSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        # invalid identity document number
        data = {
            'username': 'qux',
            'password': 'baz',
            'identity_document_number': 'B875013(0)',
        }
        serializer = UserSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        # read
        serializer = UserSerializer(user)
        with self.assertRaises(NotImplementedError):
            _ = serializer.data
