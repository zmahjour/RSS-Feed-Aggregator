from datetime import datetime
import logging
import pytz
import json


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("api_logger")

