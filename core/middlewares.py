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

    def get_request_data(self, request):
        request_data = {
            "request_time": str(datetime.now(tz=pytz.timezone("Asia/Tehran"))),
            "ip_address": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
            "method": request.method,
            "path": request.path,
            "user": request.user.username or None,
        }

        return request_data

    def get_response_data(self, response):
        response_data = {
            "response_time": str(datetime.now(tz=pytz.timezone("Asia/Tehran"))),
            "status_code": response.status_code,
        }

        return response_data
