"""Module with the Retrieval Class"""
from typing import Optional, Literal

from sprynger.utils.constants import BASE_URL
from sprynger.utils.fetch import fetch_data
from sprynger.utils.startup import get_config

class Retrieve():
    """Base class to retrieve data from the Springer API."""
    @property
    def json(self):
        """JSON response from the API."""
        return self._res.json()

    def __init__(self,
                 identifier: str,
                 id_type: Optional[Literal['doi', 'issn', 'isbn']],
                 api: Literal['metadata', 'meta/v2', 'openaccess'],
                 start: int = 1,
                 max_results: int = 10):

        config = get_config()

        self._url = f'{BASE_URL}/{api}/json'
        self._params = {'q': f'{id_type}:{identifier}',
                       's': start,
                       'p': max_results,
                       'api_key': config.get('Authentication', 'APIKey')}

        self._res = fetch_data(url=self._url, params=self._params)
