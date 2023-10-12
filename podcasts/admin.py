from django.contrib import admin
from .models import Rss, Category, Channel, Episode


admin.site.register(Rss)
admin.site.register(Category)
admin.site.register(Channel)
admin.site.register(Episode)
