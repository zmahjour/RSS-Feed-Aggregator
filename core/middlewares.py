from datetime import datetime
import logging
import pytz
import json


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("api_logger")

    def __call__(self, request):
        request_data = self.get_request_data(request)
        response = self.get_response(request)
        response_data = self.get_response_data(response)
        log_data = {"request": request_data, "response": response_data}
        self.logger.info(json.dumps(log_data))

        return response

