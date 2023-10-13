from django.contrib import admin
from .models import Subscription, Favorite, Comment, Playlist, Bookmark, Notification


admin.site.register(Subscription)
admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(Playlist)
admin.site.register(Bookmark)
admin.site.register(Notification)
