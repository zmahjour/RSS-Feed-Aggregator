from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from .serializers import RssSerializer, ChannelSerializer, EpisodeSerializer
from .models import Rss, Channel, Episode
from .tasks import create_or_update_one_channel_task, create_or_update_all_channels_task
from core.pagination import CustomPagination


class RssView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serialized_data = RssSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            rss_url = serialized_data.validated_data["rss_url"]

            try:
            except IntegrityError:
class CreateOrUpdateOneChannelView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serialized_data = RssSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            rss_url = serialized_data.validated_data["rss_url"]

            create_or_update_one_channel_task.delay(rss_url=rss_url)

            return Response(
                data={"message": _("The channel is going to be updated.")},
                status=status.HTTP_202_ACCEPTED,
            )


class CreateOrUpdateAllChannelsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        create_or_update_all_channels_task.delay()

        return Response(

class ListOfChannelsView(generics.ListAPIView):
    authentication_classes = []
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    pagination_class = CustomPagination

