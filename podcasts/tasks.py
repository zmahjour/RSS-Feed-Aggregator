from celery import shared_task, Task
from celery.utils.log import get_task_logger
from django.db import transaction
from .parser import create_or_update
from .models import Rss


logger = get_task_logger(__name__)


class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = 2
    retry_jitter = False


@shared_task(base=BaseTaskWithRetry)
def create_or_update_task(rss_url):
    create_or_update(rss_url=rss_url)
