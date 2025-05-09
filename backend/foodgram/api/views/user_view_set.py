from django.contrib.auth import get_user_model
from djoser import views
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from subscriptions.subscription_actions_mixin import SubscriptionActionsMixin
from ..serializers import AvatarSerializer
from foodgram import permissions


class UserViewSet(views.UserViewSet, SubscriptionActionsMixin):
    queryset = get_user_model().objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnlyAndNotMe,)


    @action(
        detail=False,
        methods=('put', 'delete'),
        url_path='me/avatar',
        permission_classes=(IsAuthenticated,)
    )
    def avatar(self, request):
        match request.method:
            case 'PUT':
                return Response(self.update_avatar(request))
            case 'DELETE':
                self.remove_avatar(request.user)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return None

    @staticmethod
    def update_avatar(request):
        serializer = AvatarSerializer(
            request.user,
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def remove_avatar(user):
        if user.avatar:
            user.avatar.delete()
            user.avatar = None
            user.save()
