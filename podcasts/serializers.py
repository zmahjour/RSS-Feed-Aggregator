from rest_framework import serializers


class RssSerializer(serializers.Serializer):
    rss_url = serializers.CharField()
