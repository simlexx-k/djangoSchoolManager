import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Incoming request: {request.method} {request.path}")
        response = self.get_response(request)
        logger.info(f"Outgoing response: {response.status_code}")
        return response

