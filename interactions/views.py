from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from podcasts.models import Episode, Channel
from podcasts.serializers import ChannelSerializer, EpisodeSerializer
from .serializers import CommentSerializer
from .models import Subscription, Like, Bookmark, Playlist, Comment
from .utils import (
    create_interaction_with_generic_relation,
    delete_interaction_with_generic_relation,
)


class SubscribeChannelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, channel_id):
        user = request.user
        channel = get_object_or_404(Channel, pk=channel_id)

        if Subscription.is_subscribed(user, channel):
            return Response(
                data={"message": _("You have subscribed this channel before.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Subscription.objects.create(user=user, channel=channel)

        return Response(
            data={"message": _("You have subscribed this channel.")},
            status=status.HTTP_201_CREATED,
        )


class UnsubscribeChannelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, channel_id):
        user = request.user
        channel = get_object_or_404(Channel, pk=channel_id)

        if not Subscription.is_subscribed(user=user, channel=channel):
            return Response(
                data={"message": _("You have not subscribed this channel before.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Subscription.objects.get(user=user, channel=channel).delete()

        return Response(
            data={"message": _("You have unsubscribed this channel.")},
            status=status.HTTP_200_OK,
        )


class ListOfSubscribedChannelsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        subscribed_channels = Subscription.get_subscribed_channels(user=user)
        serialized_data = ChannelSerializer(instance=subscribed_channels, many=True)

        return Response(data=serialized_data.data, status=status.HTTP_200_OK)


class LikeEpisodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, episode_id):
        user = request.user

        return create_interaction_with_generic_relation(
            user=user,
            object_model=Episode,
            object_id=episode_id,
            interaction_model=Like,
            is_method=Like.is_liked,
            failure_message=_("You have liked this episode before."),
            success_message=_("You have liked this episode."),
        )


class UnlikeEpisodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, episode_id):
        user = request.user

        return delete_interaction_with_generic_relation(
            user=user,
            object_model=Episode,
            object_id=episode_id,
            interaction_model=Like,
            is_method=Like.is_liked,
            failure_message=_("You have not liked this episode before."),
            success_message=_("You have unliked this episode."),
        )


class ListOfLikedEpisodesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        content_type = ContentType.objects.get_for_model(Episode)
        liked_episodes = Like.get_liked_objects(user=user, content_type=content_type)
        serialized_data = EpisodeSerializer(instance=liked_episodes, many=True)

        return Response(data=serialized_data.data, status=status.HTTP_200_OK)


        user = request.user

        if not Like.is_liked(
            user=user, content_type=content_type, object_id=episode_id
        ):
            return Response(
                data={"message": _("You have not liked this episode before.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Like.objects.get(
            user=user, content_type=content_type, object_id=episode_id
        ).delete()

        return Response(
            data={"message": _("You have unliked this episode.")},
            status=status.HTTP_200_OK,
        )
