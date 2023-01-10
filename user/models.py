from datetime import datetime, timedelta

import jwt
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache import cache
from django.db import models

from basic import constants as basic_const
from user import constants as const

User = get_user_model()


def _generate_jwt_token(self: User):
    payload = {
        'pk': self.pk,
        'username': self.username,
        'email': self.email,
        'first_name': self.first_name,
        'last_name': self.last_name,
        'exp': datetime.now() + timedelta(days=1),  # Token expires one day after being created
    }
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    cache_key = const.USER_TOKEN_CACHE_KEY.format(self.pk)
    cache.set(cache_key, jwt_token, timeout=const.USER_TOKEN_CACHE_TTL)

    return jwt_token


@property
def token(self):
    return self._generate_jwt_token()


User._generate_jwt_token = _generate_jwt_token
User.token = token


class Wallet(models.Model):
    amount = models.PositiveIntegerField(default=0)
    currency = models.CharField(
        max_length=64,
        choices=basic_const.CURRENCIES.choices,
        default=basic_const.CURRENCIES.TIYN
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')

    class Meta:
        unique_together = ('user', 'currency')
