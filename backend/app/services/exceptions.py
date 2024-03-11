import werkzeug.exceptions as exceptions

# Custom exception to raise when there is a problem fetching data from an external service
class APIError(exceptions.InternalServerError):
    def __init__(self, description='There was a problem fetching data from an external service'):
        self.description = description