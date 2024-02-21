import werkzeug.exceptions as exceptions
class APIError(exceptions.InternalServerError):
    def __init__(self, description='There was a problem fetching data from an external service'):
        self.description = description