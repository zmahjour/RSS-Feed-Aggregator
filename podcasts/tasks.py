from celery import shared_task
from core.parser import create_or_update_channel_and_episodes


@shared_task(bind=True, max_retries=4, retry_backoff=4)
def create_or_update(self, rss_url):
    try:
        create_or_update_channel_and_episodes(rss_url=rss_url)
    except:
        self.retry()
