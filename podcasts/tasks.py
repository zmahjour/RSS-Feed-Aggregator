from celery import shared_task
from celery.utils.log import get_task_logger
from .models import Rss
from .parser import create_or_update


logger = get_task_logger(__name__)


# class BaseTaskWithRetry(Task):
#     autoretry_for = (TypeError,)
#     max_retries = 5
#     retry_backoff = True
#     retry_backoff_max = 700
#     retry_jitter = False


@shared_task
def read_rss_data_task():
    rss_urls = [rss.rss_url for rss in Rss.objects.all()]
    return rss_urls


# @shared_task(bind=True, max_retries=4, retry_backoff=4)
@shared_task
def create_or_update_task(rss_url):
    try:
        create_or_update(rss_url=rss_url)
    except Exception as e:
        logger.info(e)
        # self.retry()
