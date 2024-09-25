"""Utility functions for fetching data from the Springer API."""
from typing import Literal

from requests.adapters import HTTPAdapter
from requests import Response, Session
from urllib3.util.retry import Retry

from sprynger.utils.startup import get_config

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
    retries = Retry(
        total=max_retries,
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
    if status_code != 200:
        if response.status_code == 400:
            raise InvalidRequestError(response.status_code)
        elif response.status_code == 401 or response.status_code == 403:
            raise AuthenticationError(response.status_code)
        elif response.status_code == 404:
            raise ResourceNotFoundError(response.status_code)
        elif response.status_code == 429:
            raise RateLimitError(response.status_code)
        elif response.status_code == 500:
            raise InternalServerError(response.status_code)
        else:
            raise APIError(response.status_code, "Unhandled error occurred")


def fetch_data(url: str, params: dict) -> Response:
    """Fetch data from the Springer API."""
    # Get the configuration
    config = get_config()
    max_retries = config.getint('Requests', 'Retries', fallback=5)
    backoff_factor = config.getfloat('Requests', 'BackoffFactor', fallback=2.0)
    timeout = config.getint('Requests', 'Timeout', fallback=20)

    # Create session and retrieve data
    session = create_session(max_retries, backoff_factor)
    response = session.get(url, params=params, timeout=timeout)
    check_response(response)

    return response


def detect_id_type(id: str) -> Literal['doi', 'issn', 'isbn']:
    """Detect the type of identifier."""
    if id.startswith('10.'):
        return 'doi'
    elif len(id) == 9:
        return 'issn'
    elif len(id) in [14, 17]:
        return 'isbn'
    else:
        raise ValueError('Invalid identifier')
