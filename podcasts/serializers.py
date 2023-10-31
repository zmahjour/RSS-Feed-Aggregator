from rest_framework import serializers
from .models import Channel, Episode


class RssSerializer(serializers.Serializer):
    rss_url = serializers.CharField()


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = "__all__"
