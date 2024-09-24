"""Utility functions for fetching data from the Springer API."""
from typing import Literal

from requests import Response, Session

from sprynger.exceptions import APIError, AuthenticationError, InternalServerError, InvalidRequestError, RateLimitError, ResourceNotFoundError



def create_session():
    """Create a session."""
    session = Session()
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
    session = create_session()
    response = session.get(url, params=params)
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

