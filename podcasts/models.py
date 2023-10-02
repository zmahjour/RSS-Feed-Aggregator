from django.db import models


class Rss(models.Model):
    rss_url = models.URLField(max_length=500, unique=True)

    def __str__(self):
        return self.id


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Channel(models.Model):
    rss = models.OneToOneField(Rss, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    subtitle = models.TextField(null=True, blank=True)
    description = models.TextField()
    author = models.CharField(max_length=100, null=True, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=25, null=True, blank=True)
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    owner_email = models.EmailField(null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title


class Episode(models.Model):
    guid = models.TextField(unique=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subtitle = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    duration = models.CharField(max_length=10, null=True, blank=True)
    explicit = models.BooleanField(default=False)
    episode_type = models.CharField(max_length=25, null=True, blank=True)
    image_url = models.TextField(null=True, blank=True)
    audio_url = models.TextField()

    def __str__(self):
        return self.title
