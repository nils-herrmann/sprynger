"""Base class to retrieve data from the Springer API."""
from __future__ import annotations
from math import ceil
import os
import hashlib
import json
from json.decoder import JSONDecodeError
from typing import Optional, Literal, Union
from datetime import datetime, timedelta
import warnings

from lxml import etree
from requests import Response

from sprynger.utils.constants import BASE_URL, FORMAT, LIMIT, ONLINE_API
from sprynger.utils.fetch import fetch_data
from sprynger.utils.parse import chained_get
from sprynger.utils.startup import get_config, get_key

class Base:
    """Base class to retrieve data from the Springer API."""
    @property
    def _json(self) -> dict:
        """JSON response from the API."""
        return _to_json(self._res)

    @property
    def _xml(self) -> etree._Element:
        """XML response from the API."""
        return _to_xml(self._res)

    def __init__(self,
                 query: str,
                 api: Literal['Metadata', 'Meta', 'OpenAccess'],
                 start: int = 1,
                 nr_results: int = 10,
                 premium: bool = False,
                 cache: bool = True,
                 refresh: Union[bool, int] = False) -> None:

        config = get_config()

        self._api = api
        online_api = ONLINE_API[api]
        rate_limit = LIMIT['Premium'][api] if premium else LIMIT['Basic'][api]
        limit = min(nr_results, rate_limit)

        key = get_key()
        self._url = f'{BASE_URL}/{online_api}/{FORMAT[api]}'
        self._params = {'q': query,
                        's': start,
                        'p': limit,
                        'api_key': key}

        # Generate a cache key based on the parameters
        cache_dir = chained_get(config, ['Directories', api])
        cache_key = self._create_cache_key(query, start, limit)
        self._cache_file = os.path.join(cache_dir, f'{cache_key}.{FORMAT[api]}')
        self._refresh = refresh
        self._cache = cache

        self._res = self._fetch_or_load()
        n_found = self._get_total_results()

        if n_found == 0:
            warnings.warn('No results where found. Check the query.', UserWarning)

        n = min(nr_results, n_found)
        n_chunks = ceil(n / limit)
        for i in range(1, n_chunks):
            new_start = start + i * limit
            n -= limit
            limit = min(n, limit)
            # Update variables for querying the next chunk
            self._params.update({'s': new_start,
                                 'p': limit})
            cache_key = self._create_cache_key(query, new_start, limit)
            self._cache_file = os.path.join(cache_dir, f'{cache_key}.{FORMAT[api]}')
            tmp_res = self._fetch_or_load()
            self._res = self._append_response(tmp_res)


    def _create_cache_key(self, query: str, start: int, limit: int) -> str:
        """Create a cache key based on the query and start."""
        cache_key = f'{query}_{start}_{limit}'
        cache_key = hashlib.md5(cache_key.encode()).hexdigest()
        return cache_key


    def _append_response(self, tmp_res: Union[Response, MockResponse]):
        """Append the response to the current response."""
        if FORMAT[self._api] == 'json':
            data_json = _to_json(self._res)
            tmp_res_json = _to_json(tmp_res)
            # Append the records from the tmp response to the current response
            data_json['records'].extend(tmp_res_json.get('records', []))
            return MockResponse(data_json)
        elif FORMAT[self._api] == 'jats':
            data_xml = _to_xml(self._res)
            tmp_res_xml = _to_xml(tmp_res)
            # Append the records from the tmp response to the current response
            data_records = data_xml.find('./records')
            tmp_res_records = tmp_res_xml.find('./records')
            for record in tmp_res_records:
                data_records.append(record)
            data_xml_str = etree.tostring(data_xml, encoding='unicode')
            return MockResponse(data_xml_str, is_xml=True)
        else:
            raise ValueError(f'Unknown format: {FORMAT[self._api]}')

    def _fetch_or_load(self) -> Union[Response, MockResponse]:
        """Fetch or load the data from the cache."""
        if self._should_fetch():
            res = self._fetch()
        else:
            res = self._load_from_cache()
        return res

    def _get_total_results(self):
        """Get the total number of results for the query."""
        if (self._api == 'Metadata') or (self._api == 'Meta'):
            res_json = _to_json(self._res)
            total = res_json['result'][0]['total']
        elif self._api in ['OpenAccess']:
            res_xml = _to_xml(self._res)
            total = res_xml.find('./result/total').text
        else:
            raise ValueError(f'Unknown API: {self._api}')
        return int(total)

    def _should_fetch(self) -> bool:
        """Determine whether the data has to be fetched."""
        if isinstance(self._refresh, bool) and self._is_cached():
            return self._refresh # If is cached user decides to fetch
        elif isinstance(self._refresh, int) and self._is_cached():
            cache_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(self._cache_file))
            return cache_age > timedelta(days=self._refresh)  #Fetch if cache is older than specified days
        return True  # If no cache exists, return True to fetch

    def _is_cached(self) -> bool:
        """Check if the cache file exists."""
        return os.path.exists(self._cache_file)

    def _load_from_cache(self) -> MockResponse:
        """Load response from the cache."""
        with open(self._cache_file, 'r') as f:
            if FORMAT[self._api] == 'json':
                return MockResponse(json.load(f))
            elif FORMAT[self._api] == 'jats':  # XML-based format
                return MockResponse(f.read(), is_xml=True)
            else:
                raise ValueError(f'Unknown format: {FORMAT[self._api]}')

    def _fetch(self) -> Response:
        """Fetch data from the API and cache the response."""
        res = fetch_data(url=self._url, params=self._params)
        if self._cache:
            # Save the response to the cache file depending on format
            with open(self._cache_file, 'w') as f:
                if FORMAT[self._api] == 'json':
                    json.dump(res.json(), f)
                elif FORMAT[self._api] == 'jats':  # XML-based format
                    f.write(res.content.decode())
        return res

def _to_json(response) -> dict:
    """Auxiliary method to convert the response to JSON."""
    try:
        return response.json()
    except JSONDecodeError:
        return {}

def _to_xml(response) -> etree._Element:
    """Auxiliary method to convert the response to XML."""
    return etree.fromstring(text=response.content)


class MockResponse:
    """Mock response class for cached data."""
    def __init__(self, data: Union[dict, str], is_xml: bool = False) -> None:
        """Initialize the cached response, either JSON or XML (JATS)."""
        self._data = data
        self.is_xml = is_xml

    def json(self) -> Optional[dict]:
        """Return the JSON data if it's JSON."""
        if not self.is_xml:
            return self._data
        return None

    @property
    def content(self) -> str:
        """Return the raw content (used for XML parsing if needed)."""
        if self.is_xml:
            return self._data
        return json.dumps(self._data)
