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

