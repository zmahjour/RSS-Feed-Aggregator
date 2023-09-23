from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Channel(models.Model):
    rss_url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    subtitle = models.TextField(null=True, blank=True)
    description = models.TextField()
    author = models.CharField(max_length=100, null=True, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=25, null=True, blank=True)
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    owner_email = models.CharField(max_length=255, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title


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

    def __str__(self):
        return self.title
