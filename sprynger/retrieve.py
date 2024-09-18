"""Module with the Retrieval Class"""
import os
import json
from json.decoder import JSONDecodeError
from typing import Optional, Literal, Union
from datetime import datetime, timedelta

from lxml import etree

from sprynger.utils.constants import BASE_URL, FORMAT
from sprynger.utils.fetch import fetch_data
from sprynger.utils.startup import get_config



class Retrieve():
    """Base class to retrieve data from the Springer API."""
    @property
    def json(self) -> Optional[dict]:
        """JSON response from the API."""
        if FORMAT[self._api] == 'json':
            try:
                return self._res.json()
            except JSONDecodeError:
                return {}
        return None

    @property
    def xml(self) -> Optional[etree._Element]:
        """XML response from the API."""
        if FORMAT[self._api] == 'jats':
            return etree.fromstring(text=self._res.content)
        return None

    def __init__(self,
                 identifier: str,
                 id_type: Optional[Literal['doi', 'issn', 'isbn']],
                 api: Literal['Metadata', 'Meta', 'OpenAccess'],
                 start: int = 1,
                 max_results: int = 10,
                 cache: bool = True,
                 refresh: Union[bool, int] = False) -> None:

        config = get_config()

        self._api = api
        self._url = f'{BASE_URL}/{api.lower()}/{FORMAT[api]}'
        self._params = {'q': f'{id_type}:{identifier}',
                       's': start,
                       'p': max_results,
                       'api_key': config.get('Authentication', 'APIKey')}

        # Generate a cache key based on the parameters
        cache_dir = config.get('Directories', api)
        self._cache_key = f'{identifier.replace("/", "-")}_{start}_{max_results}'
        self._cache_file = os.path.join(cache_dir, f'{self._cache_key}.{FORMAT[api]}')

        if self._should_fetch(refresh):
            self._fetch(cache)
        else:
            self._load_from_cache()

    def _should_fetch(self, refresh: Union[bool, int]) -> bool:
        """Determine whether the data has to be fetched."""
        if isinstance(refresh, bool) and self._is_cached():
            return refresh # If is cached user decides to fetch
        elif isinstance(refresh, int) and self._is_cached():
            cache_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(self._cache_file))
            return cache_age > timedelta(days=refresh)  #Fetch if cache is older than specified days
        return True  # If no cache exists, return True to fetch

    def _is_cached(self) -> bool:
        """Check if the cache file exists."""
        return os.path.exists(self._cache_file)

    def _load_from_cache(self) -> None:
        """Load response from the cache."""
        with open(self._cache_file, 'r') as f:
            if FORMAT[self._api] == 'json':
                self._res = CachedResponse(json.load(f))
            elif FORMAT[self._api] == 'jats':  # XML-based format
                self._res = CachedResponse(f.read(), is_xml=True)

    def _fetch(self, cache: bool) -> None:
        """Fetch data from the API and cache the response."""
        self._res = fetch_data(url=self._url, params=self._params)

        if cache:
            # Save the response to the cache file depending on format
            with open(self._cache_file, 'w') as f:
                if FORMAT[self._api] == 'json':
                    json.dump(self._res.json(), f)
                elif FORMAT[self._api] == 'jats':  # XML-based format
                    f.write(self._res.content.decode())


class CachedResponse:
    """Mock response class for cached data."""
    def __init__(self, data: Union[dict, str], is_xml: bool = False) -> None:
        """Initialize the cached response, either JSON or XML (JATS)."""
        if is_xml:
            self._data = data  # Raw XML content
            self.is_xml = True
        else:
            self._data = data  # Parsed JSON
            self.is_xml = False

    def json(self) -> Optional[dict]:
        """Return the JSON data if it's JSON."""
        if not self.is_xml:
            return self._data
        return None

    @property
    def content(self) -> bytes:
        """Return the raw content (used for XML parsing if needed)."""
        if self.is_xml:
            return self._data.encode()
        return json.dumps(self._data).encode()

