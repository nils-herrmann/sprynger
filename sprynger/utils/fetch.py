"""Utility functions for fetching data from the Springer API."""
from requests.adapters import HTTPAdapter
from requests import Response, Session
from urllib3.util.retry import Retry

from sprynger.utils.startup import get_config
from sprynger.utils.parse import chained_get

from sprynger.exceptions import (
    APIError,
    AuthenticationError,
    InternalServerError,
    InvalidRequestError,
    RateLimitError,
    ResourceNotFoundError,
)


def create_session(max_retries: int,
                   backoff_factor: float) -> Session:
    """Create a session."""
    session = Session()
    retries = Retry(total=max_retries,
        backoff_factor=backoff_factor,
        backoff_max=60,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def check_response(response: Response) -> None:
    """Check the response."""
    status_code = response.status_code

    error_map = {
        400: InvalidRequestError,
        401: AuthenticationError,
        403: AuthenticationError,
        404: ResourceNotFoundError,
        429: RateLimitError,
        500: InternalServerError
    }

    if status_code != 200:
        error_class = error_map.get(status_code, APIError)
        if error_class is APIError:
            raise error_class(status_code, "Unhandled error occurred")
        raise error_class(status_code)


def fetch_data(url: str, params: dict) -> Response:
    """Fetch data from the Springer API."""
    # Get the configuration
    config = get_config()
    max_retries = int(chained_get(config, ['Requests', 'Retries'], 5))
    backoff_factor = float(chained_get(config, ['Requests', 'BackoffFactor'], 2.0))
    timeout = int(chained_get(config, ['Requests', 'Timeout'], 20))

    # Create session and retrieve data
    session = create_session(max_retries, backoff_factor)
    response = session.get(url, params=params, timeout=timeout)
    check_response(response)

    return response
