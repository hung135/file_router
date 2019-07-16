class ExitProjectException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class InvalidAPIVersion(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message