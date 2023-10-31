from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .tasks import create_or_update_one_channel_task, create_or_update_all_channels_task


class RssView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serialized_data = RssSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            rss_url = serialized_data.validated_data["rss_url"]

            try:
            except IntegrityError:
            return Response(
                data={"message": "New Rss instance created."},
                status=status.HTTP_201_CREATED,
            )


class CreateOrUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        create_or_update_task.delay()
        return Response(
            data={"message": "All podcasts have been updated."},
            status=status.HTTP_200_OK,
        )
