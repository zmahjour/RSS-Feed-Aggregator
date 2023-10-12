from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.db import transaction
from .serializers import RssSerializer
from .models import Rss
from .tasks import create_or_update_task


class RssView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serialized_data = RssSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            rss_url = serialized_data.validated_data["rss_url"]
            Rss.objects.create(rss_url=rss_url)
            return Response(
                data={"message": "New Rss instance created."},
                status=status.HTTP_201_CREATED,
            )


class CreateOrUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        rss_urls = [rss.rss_url for rss in Rss.objects.all()]
        for rss_url in rss_urls:
            with transaction.atomic():
                try:
                    create_or_update_task.delay(rss_url=rss_url)
                    print(f"Podcast with '{rss_url}' url updated successfully.")
                except Exception as e:
                    print(f"error: {str(e)}")
        return Response(
            data={"message": "All podcasts have been updated."},
            status=status.HTTP_200_OK,
        )
