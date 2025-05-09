from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers import UserWithRecipesSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from .subscription_manage import subscribe, unsubscribe


class SubscriptionActionsMixin:

    @action(
        methods=['get'],
        detail=False,
        url_path='subscriptions',
        url_name='subscriptions',
        permission_classes=(IsAuthenticated,),
    )
    def get_subscriptions(self, request):
        subs = request.user.subscriptions.all()
        sub_users = [s.author for s in subs]
        page = self.paginate_queryset(sub_users)
        if page is not None:
            serializer = UserWithRecipesSerializer(
                page,
                many=True,
                context={
                    'request': request,
                    'recipes_limit': self.get_recipes_limit(request)},
            )
            return self.get_paginated_response(serializer.data)
        serializer = UserWithRecipesSerializer(
            sub_users,
            many=True,
            context={
                'request': request,
                'recipes_limit': self.get_recipes_limit(request)},
        )
        return Response(serializer.data)



    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='subscribe',
        url_name='subscribe',
        permission_classes=(IsAuthenticated,),
    )
    def subscription(self, request, id):
        user = request.user
        author = get_object_or_404(get_user_model(), pk=id)
        match request.method:
            case 'POST':
                serializer = UserWithRecipesSerializer(
                    subscribe(user, author),
                    context={
                        'request': request,
                        'recipes_limit': self.get_recipes_limit(request)},
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            case 'DELETE':
                unsubscribe(user, author)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return None

    def get_recipes_limit(self, request):
        return int(request.query_params.get('recipes_limit', 10))