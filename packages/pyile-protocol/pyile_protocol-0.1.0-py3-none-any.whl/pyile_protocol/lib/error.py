class AuthenticationException(Exception):
    def __init__(self, message):
        super().__init__(message)


class StatusException(Exception):
    def __init__(self, message):
        super().__init__(message)


class SendException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RecvException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ConnectionException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ThreadException(Exception):
    def __init__(self, message):
        super().__init__(message)
