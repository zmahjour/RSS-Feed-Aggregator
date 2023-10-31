from celery import Task, states
import logging
import json


logger = logging.getLogger("celery_logger")


class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = 2
    retry_jitter = False

