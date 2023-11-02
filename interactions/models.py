from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from accounts.models import User
from podcasts.models import Channel


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} subscribed {self.channel}"

    @classmethod
    def is_subscribed(cls, user, channel):
        return cls.objects.filter(user=user, channel=channel).exists()

    @classmethod
    def get_subscribed_channels(cls, user):
        subscribed_channels = Channel.objects.filter(
            pk__in=cls.objects.filter(user=user).values_list("channel", flat=True)
        )
        return subscribed_channels


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return str(self.id)

    @classmethod
    def is_liked(cls, user, content_type, object_id):
        return cls.objects.filter(
            user=user, content_type=content_type, object_id=object_id
        ).exists()

    @classmethod
    def get_liked_objects(cls, user, content_type):
        model = content_type.model_class()
        liked_objects = model.objects.filter(
            pk__in=cls.objects.filter(user=user, content_type=content_type).values_list(
                "object_id", flat=True
            )
        )
        return liked_objects


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_item_comments(cls, content_type, object_id):
        commetns = cls.objects.filter(content_type=content_type, object_id=object_id)
        return commetns


class Playlist(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist = models.ForeignKey(
        Playlist, on_delete=models.SET_NULL, null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return str(self.id)

    @classmethod
    def is_bookmarked(cls, user, content_type, object_id):
        return cls.objects.filter(
            user=user, content_type=content_type, object_id=object_id
        ).exists()

    @classmethod
    def get_bookmarked_objects(cls, user, content_type):
        model = content_type.model_class()
        bookmarked_objects = model.objects.filter(
            pk__in=cls.objects.filter(user=user, content_type=content_type).values_list(
                "object_id", flat=True
            )
        )
        return bookmarked_objects


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.content
