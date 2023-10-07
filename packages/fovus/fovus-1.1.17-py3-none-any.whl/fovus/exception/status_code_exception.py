class StatusException(Exception):
    def __init__(self, status_code, source, message=""):
        self.status_code = status_code
        self.source = source
        self.message = message

    def __str__(self):
        return f"{str(self.status_code)} from {self.source}. {self.message}"
