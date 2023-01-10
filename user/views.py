from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response

from user import serializers

User = get_user_model()


class SignUpViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):

    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.SignUpSerializer
    permission_classes = (permissions.AllowAny,)


class SignInViewSet(viewsets.GenericViewSet):

    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.SignInSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
