from celery import shared_task
from .models import Rss
from .parser import create_or_update


@shared_task
def read_rss_data_task():
    rss_urls = [rss.rss_url for rss in Rss.objects.all()]
    return rss_urls


    try:
        create_or_update(rss_url=rss_url)
    except Exception as e:
        print(e)
        self.retry()
