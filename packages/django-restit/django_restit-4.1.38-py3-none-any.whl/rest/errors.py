
class RestError(Exception):
    def __init__(self, reason, code=None):
        self.reason = reason
        self.code = code

    def __repr__(self):
        return self.reason


class PermissionDeniedException(RestError):
    def __init__(self, reason="permission denied", code=401):
        self.reason = reason
        self.code = code


class RestValidationError(RestError):
    def __init__(self, reason="rest data is not valid", code=123):
        self.reason = reason
        self.code = code
