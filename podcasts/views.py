from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import RssSerializer
from .models import Rss
from .tasks import read_rss_data_task, create_or_update_task


class RssView(APIView):
    def post(self, request):
        serialized_data = RssSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            rss_url = serialized_data.validated_data["rss_url"]
            Rss.objects.create(rss_url=rss_url)
            return Response(
                data={"message": "New Rss instance created."},
                status=status.HTTP_201_CREATED,
            )
