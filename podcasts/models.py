from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)


class Channel(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(null=True, blank=True)
    description = models.TextField()
    author = models.CharField(max_length=100)
    pubdate = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=10)
    owner_name = models.CharField(max_length=100)
    owner_email = models.CharField(max_length=255)
    image_url = models.TextField(null=True, blank=True)
    rss_feed = models.TextField()
    categories = models.ManyToManyField(Category)


class Episode(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    subtitle = models.TextField(null=True, blank=True)
    description = models.TextField()
    author = models.CharField(max_length=100, null=True, blank=True)
    pubdate = models.DateTimeField()
    duration = models.CharField(max_length=10)
    episode_type = models.CharField(max_length=25)
    guid = models.TextField()
    image_url = models.TextField(null=True, blank=True)
    audio_url = models.TextField()
