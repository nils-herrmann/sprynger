"""Module with the Retrieval Class"""
from typing import Optional, Literal, Union

from sprynger.base import Base
from sprynger.utils.constants import VALID_FIELDS



class Retrieve(Base):
    """Retrieve data from the Springer API."""
    def _check_query(self,
                    query: str,
                    kwargs: Optional[dict],
                    api: Literal['OpenAccess', 'Meta', 'Metadata'],
                    plan: Literal['Basic', 'Premium']) -> None:
        """Auxiliary function to check if the query and kwargs are valid."""
        # Either query or kwargs should be provided
        if not query and not kwargs:
            raise ValueError("Please provide a query or kwargs.")
        # Check if kwargs are valid
        if kwargs:
            for field in kwargs:
                if field not in VALID_FIELDS:
                    raise ValueError(f"Invalid field: {field}.")
                if api not in VALID_FIELDS[field].get('api'):
                    raise ValueError(f"Field {field} is not available in {api}.")
                if plan not in VALID_FIELDS[field].get('plan'):
                    raise ValueError(f"Field {field} is not available in {plan} plan.")


    def _build_filters(self, kwargs: dict) -> str:
        """Auxiliary function to build filters for the query."""
        filters = ''
        if kwargs:
            for field, value in kwargs.items():
                if isinstance(value, list):
                    filters += ' '.join(f'{field}:{v}' for v in value)
                else:
                    filters = self._and_join(filters, f'{field}:{value}')
        return filters

    def _and_join(self,
                  str1: str,
                  str2: str) -> str:
        """Auxiliary function to join two strings with AND"""
        if str1 and str2:  # Both strings are non-empty
            return f"{str1} {str2}"
        return str1 or str2


    def __init__(self,
                 query: str,
                 api: Literal['Metadata', 'Meta', 'OpenAccess'],
                 start: int = 1,
                 nr_results: int = 10,
                 premium: bool = False,
                 cache: bool = True,
                 refresh: Union[bool, int] = False,
                 **kwargs):
        """This class handles the query to retrieve the data from the Springer API."""

        plan = 'Premium' if premium else 'Basic'
        self._check_query(query, kwargs, api, plan)
        filters = self._build_filters(kwargs)
        query = self._and_join(query, filters)

        super().__init__(query=query,
                         api=api,
                         start=start,
                         nr_results=nr_results,
                         premium=premium,
                         cache=cache,
                         refresh=refresh)


