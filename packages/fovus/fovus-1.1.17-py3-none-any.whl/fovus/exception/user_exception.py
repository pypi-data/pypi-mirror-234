from fovus.exception.status_code_exception import StatusException


class UserException(StatusException):
    def __str__(self):
        return "Error: " + super().__str__()
