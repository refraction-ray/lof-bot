class LOFException(Exception):
    def __repr__(self):
        return self.reason

    __str__ = __repr__


class DateMismatch(LOFException):
    def __init__(self, code, reason=""):
        self.code = code
        self.reason = reason


class NonAccurate(LOFException):
    def __init__(self, code, reason=""):
        self.code = code
        self.reason = reason
