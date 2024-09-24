"""Module with the Exceptions Classes"""

class APIError(Exception):
    """Base class for API errors"""
    def __init__(self, status_code, message="An error occurred with the API request"):
        self.status_code = status_code
        self.message = message
        super().__init__(f"{status_code}: {message}")


class AuthenticationError(APIError):
    """Exception raised for 401/403 Authentication Failures"""
    def __init__(self, status_code, message="Authentication failed. Check your API key."):
        super().__init__(status_code, message)


class RateLimitError(APIError):
    """Exception raised for 429 Rate Limit Exceeded"""
    def __init__(self, status_code, message="Rate limit exceeded. Try again later."):
        super().__init__(status_code, message)


class ResourceNotFoundError(APIError):
    """Exception raised for 404 Resource Not Found"""
    def __init__(self, status_code, message="Resource not found. Check your URL or query."):
        super().__init__(status_code, message)


class InvalidRequestError(APIError):
    """Exception raised for 400 Bad Request due to invalid formats"""
    def __init__(self, status_code, message="Invalid request format. Check your parameters."):
        super().__init__(status_code, message)


class InternalServerError(APIError):
    """Exception raised for 500 Internal Server Error"""
    def __init__(self, status_code, message="Internal server error. Try again later."):
        super().__init__(status_code, message)
