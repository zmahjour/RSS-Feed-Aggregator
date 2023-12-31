from django.db import transaction
from celery import shared_task
from core.base_task import BaseTaskWithRetry
from .parser import create_or_update
from .models import Rss


@shared_task(bind=True, base=BaseTaskWithRetry)
def create_or_update_one_channel_task(self, rss_url):
    with transaction.atomic():
        create_or_update(rss_url=rss_url)


@shared_task(bind=True, base=BaseTaskWithRetry)
def create_or_update_all_channels_task(self):
    rss_urls = [rss.rss_url for rss in Rss.objects.all()]

    for rss_url in rss_urls:
        try:
            create_or_update_one_channel_task.delay(rss_url=rss_url)
            print(f"Podcast with '{rss_url}' url updated successfully.")
        except Exception as e:
            print(f"error: {str(e)}")
