from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RssSerializer
from core.parser import create_update_channel_episodes


class RssView(APIView):
    def post(self, request):
        serialized_data = RssSerializer(data=request.data)
        if serialized_data.is_valid():
            rss_url = serialized_data.validated_data["rss_url"]
            create_update_channel_episodes(rss_url=rss_url)
            return Response(
                data={"message": "Podcast updated successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(data=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
