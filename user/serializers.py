import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    def validate_identity_document_number(self, value):
        error = ValidationError('Invalid identity document number')
        regex = re.compile(r'^[A-Z]{1,2}[\d]{6}\([\d]\)$', re.I)
        ord_offset = 55

        if not regex.match(value):
            raise error

        try:
            if len(value) == 11:  # ensured the length is 10-11 in regex
                letter_1 = ord(value[0]) - ord_offset
            else:
                value = ' ' + value
                letter_1 = 36
            letter_2 = ord(value[1]) - ord_offset
            sum_of_digits = sum(
                int(digit) * coefficient
                for digit, coefficient in zip(value[2:8], range(7, 1, -1))
            ) + letter_1 * 9 + letter_2 * 8
            remainder = sum_of_digits % 11
            if remainder == 0:
                pass
            elif remainder == 1 and int(value[-2]) == 'A':
                pass
            elif 11 - remainder == int(value[-2]):
                pass
            else:
                raise error
        except ValueError:
            raise error

        return value.strip()

    def to_representation(self, instance):
        raise NotImplementedError

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'identity_document_number',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'identity_document_number': {'write_only': True},
        }
