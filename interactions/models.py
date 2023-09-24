from django.db import models

from accounts.models import User
from podcasts.models import Channel, Episode


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} subscribed {self.channel}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} added {self.episode} to favorites"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET("deleted account"))
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    reply = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user} commented on {self.episode}"


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    episodes = models.ManyToManyField(Episode)
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} created {self.title} playlist"
