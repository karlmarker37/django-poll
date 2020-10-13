import uuid

import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for base user info"""

    id = factory.LazyAttribute(lambda x: uuid.uuid4())
    password = 'wuwW^&d2hS212ewedw'

    email = factory.LazyAttribute(lambda user: f'{user.id}@hello.com')

    class Meta:
        model = User
