"""Module with the Retrieval Class"""
from json.decoder import JSONDecodeError
from typing import Optional, Literal

from lxml import etree

from sprynger.utils.constants import BASE_URL, FORMAT
from sprynger.utils.fetch import fetch_data
from sprynger.utils.startup import get_config



class Retrieve():
    """Base class to retrieve data from the Springer API."""
    @property
    def json(self) -> dict:
        """JSON response from the API."""
        try:
            return self._res.json()
        except JSONDecodeError:
            return {}

    @property
    def xml(self) -> etree._Element:
        """XML response from the API."""
        return etree.fromstring(text = self._res.content)

    def __init__(self,
                 identifier: str,
                 id_type: Optional[Literal['doi', 'issn', 'isbn']],
                 api: Literal['Metadata', 'Meta', 'OpenAccess'],
                 start: int = 1,
                 max_results: int = 10):

        config = get_config()

        self._url = f'{BASE_URL}/{api.lower()}/{FORMAT[api]}'

        self._params = {'q': f'{id_type}:{identifier}',
                       's': start,
                       'p': max_results,
                       'api_key': config.get('Authentication', 'APIKey')}

        self._res = fetch_data(url=self._url, params=self._params)
