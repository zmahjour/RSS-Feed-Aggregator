from celery import Task, states
import logging
import json


logger = logging.getLogger("celery_logger")


class BaseTaskWithRetry(Task):
    autoretry_for = (Exception,)
    max_retries = 5
    retry_backoff = 2
    retry_jitter = False

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        retries = self.request.retries + 1
        log_data = {
            "task": self.name,
            "task_id": task_id,
            "state": states.RETRY,
            "retries": retries,
            "warning": str(exc),
        }
        logger.warning(json.dumps(log_data))

