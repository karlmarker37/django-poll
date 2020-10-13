from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.urls import reverse, NoReverseMatch
from rest_framework.test import APITestCase

from user.tests.factories import UserFactory

User = get_user_model()


class TestUserViewSet(APITestCase):
    def test_create_user(self):
        view_name = 'v1:user-list'
        
        payload = {
            'username': 'foo',
            'password': 'bar',
            'identity_document_number': 'B875013(6)',
        }
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(reverse(view_name), data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        new_user = User.objects.order_by('-create_date').first()
        self.assertEqual(new_user.username, 'foo')
        self.assertNotEqual(new_user.password, 'bar')  # hashed
        self.assertTrue(check_password('bar', new_user.password))
        self.assertEqual(new_user.identity_document_number, 'B875013(6)')

    def test_retrieve_user(self):
        user = UserFactory.create()
        view_name = 'v1:user-detail'

        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse(view_name, kwargs={'pk': str(user.id)}))
