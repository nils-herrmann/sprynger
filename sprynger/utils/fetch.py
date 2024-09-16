from requests import Response, Session

from typing import Literal

def create_session():
    session = Session()
    return session

def fetch_data(url: str, params: dict) -> Response:
    """Fetch data from the Springer API."""
    session = create_session()
    response = session.get(url, params=params)

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

