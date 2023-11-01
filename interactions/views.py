from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from podcasts.models import Episode
from .models import Like


class LikeEpisodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, episode_id):
        content_type = get_object_or_404(ContentType, model="episode")
        episode = get_object_or_404(Episode, pk=episode_id)
        user = request.user

        if Like.is_liked(user=user, content_type=content_type, object_id=episode_id):
            return Response(
                data={"message": _("You have liked this episode before.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Like.objects.create(user=user, content_object=episode)

        return Response(
            data={"message": _("You have liked this episode.")},
            status=status.HTTP_201_CREATED,
        )


class UnlikeEpisodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, episode_id):
        content_type = get_object_or_404(ContentType, model="episode")
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
