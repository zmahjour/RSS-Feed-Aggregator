from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RssSerializer
from .tasks import create_or_update


class RssView(APIView):
    def post(self, request):
        serialized_data = RssSerializer(data=request.data)
        if serialized_data.is_valid():
            rss_url = serialized_data.validated_data["rss_url"]
            create_or_update.apply_async(kwargs={"rss_url": rss_url})
            return Response(
                data={"message": "Podcast updated successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(data=serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
