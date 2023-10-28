from django.conf import settings
from datetime import datetime
from elasticsearch import Elasticsearch
import logging
import pytz
import json


class ElasticsearchHandler(logging.Handler):
    def __init__(self, prefix, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.prefix = prefix
        self.es = Elasticsearch(
            f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}"
        )

    @property
    def index_name(self):
        date = datetime.now(tz=pytz.timezone("Asia/Tehran")).strftime("%Y-%m-%d")
        return f"{self.prefix}-{date}"

    @property
    def timestamp(self):
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    def emit(self, record):
        try:
            log_data = json.loads(self.format(record))
            log_data["@timestamp"] = self.timestamp
            log_data["log_level"] = record.levelname

            self.es.index(index=self.index_name, document=log_data)

        except Exception as e:
            self.es.index(
                index=self.index_name,
                document={"@timestamp": self.timestamp, "error": e},
            )
