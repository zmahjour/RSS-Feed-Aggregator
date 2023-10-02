from celery import shared_task
from .parser import create_or_update


@shared_task(bind=True, max_retries=4, retry_backoff=4)
def create_or_update_task(self, rss_url):
    try:
        create_or_update(rss_url=rss_url)
    except Exception as e:
        print(e)
        self.retry()
