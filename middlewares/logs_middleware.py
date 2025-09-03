import time
import logging
import json

from django.http import HttpRequest


logger = logging.getLogger(__name__)


class LogsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        t = time.localtime()
        current_time = time.strftime('%H:%M:%S', t)
        time_start = time.time()
        try:
            request_body = request.body.decode('utf-8').replace('\n', ' ')
            log_request = f"{request.path} {request.method} {request.user}" +\
                f"{request_body}"
            response = self.get_response(request)
        except Exception as ex:
            response = self.get_response(request)
            log_request = str(ex)

        time_stop = time.time()
        work_time = round(time_stop - time_start, 4)

        if request.path == '/api/v1/login/':
            return response

        response_error = ""
        if response.status_code >= 400 and hasattr(response, "data"):
            response_error = "ERROR: " + \
                response.content.decode('utf-8').replace('\n', ' ')
        log_response = f"{response.status_code} {response_error}"
        log_work_time = f"{work_time}"

        answer_log = {
            'current_time': current_time,
            'user': str(request.user),
            'request': log_request,
            'response': log_response,
            'work_time': log_work_time}
        logger.info(json.dumps(answer_log))

        return response
