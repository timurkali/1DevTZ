import calendar
import jwt
from datetime import datetime

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache import cache
from rest_framework import authentication, exceptions

from user import constants as const

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    auth_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()

        if any([
            not auth_header,
            len(auth_header) != 2,
        ]):
            return None

        prefix = auth_header[0].decode('utf-8')
        jwt_token = auth_header[1].decode('utf-8')

        if prefix.lower() != self.auth_prefix.lower():
            return None

        return self._authenticate_credentials(jwt_token)

    def _authenticate_credentials(self, jwt_token):
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms='HS256')
        except Exception as e:  # noqa
            raise exceptions.AuthenticationFailed('Invalid token')

        try:
            user = User.objects.get(pk=payload['pk'], is_active=True)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        cache_key = const.USER_TOKEN_CACHE_KEY.format(user.pk)
        cached_jwt_token = cache.get(cache_key)

        if not cached_jwt_token:
            raise exceptions.AuthenticationFailed('Token expired')

        if cached_jwt_token != jwt_token:
            raise exceptions.AuthenticationFailed('Invalid token')

        current_datetime = datetime.now()
        current_unix = calendar.timegm(current_datetime.timetuple())

        if payload['exp'] < current_unix:
            raise exceptions.AuthenticationFailed('Token expired')

        return user, jwt_token
