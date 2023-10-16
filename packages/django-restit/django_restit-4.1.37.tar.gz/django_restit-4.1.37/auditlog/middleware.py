from rest import settings
from .models import PersistentLog

DEBUG_REST_ALL = settings.get("DEBUG_REST_ALL", False)
DEBUG_REST_END_POINTS = settings.get("DEBUG_REST_END_POINTS", [])
IGNORE_REST_END_POINTS = settings.get("IGNORE_REST_END_POINTS", [])


def checkRestDebug(request):
    if DEBUG_REST_ALL:
        return True
    for ep in DEBUG_REST_END_POINTS:
        if request.path.startswith(ep):
            return not checkRestIgnore(request)
    return False


def checkRestIgnore(request):
    for ep in IGNORE_REST_END_POINTS:
        if isinstance(ep, tuple):
            method, ep = ep
            return request.method == method and request.path.startswith(ep)
        if request.path.startswith(ep):
            return True
    return False


class LogRequest(object):
    last_request = None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.process_request(request)

    def process_request(self, request):
        # LogRequest.last_request = request
        request.rest_debug = False
        if request.path.startswith("/rpc/"):
            request.rest_debug = checkRestDebug(request)
            if request.rest_debug:
                request.DATA.log()
        response = self.get_response(request)
        return response

