"""
Module with Metadata class.
"""
from typing import Union

from sprynger.retrieve import Retrieve
from sprynger.utils.data_structures import (MetadataCreator,
                                            MetadataFacets,
                                            MetadataRecord,
                                            MetadataResult)
from sprynger.utils.parse import make_int_if_possible, str_to_bool


class Metadata(Retrieve):
    """Class to retreive the metadata of a document from the Springer Metadata API."""
    @property
    def facets(self) -> list[MetadataFacets]:
        """Faceted information about the results.

        Returns:
            list[MetadataFacets]: A list of MetadataFacets objects containing the 
            `facet`, `value`, and `count`.
        """
        facets_list = []
        factets = self._json.get('facets', [])
        for facet in factets:
            facet_name = facet.get('name')
            for item in facet.get('values', []):
                new_facet = MetadataFacets(facet=facet_name,
                                           value=item.get('value'),
                                           count=make_int_if_possible(item.get('count')))
                facets_list.append(new_facet)
        return facets_list

    @property
    def json(self) -> dict:
        """Raw JSON response from the Springer Metadata API."""
        return self._json

    @property
    def results(self) -> MetadataResult:
        """Overview of the results of the query.

        Returns:
            MetadataResult: An object containing the the `total` matches found, `start` 
            index of the first result, max `pageLength` when paginating and the number of 
            `recordsRetrieved`.
        """
        res = self._json.get('result', [{}])[0]
        total_results = int(res.get('total', 0))
        nr_results = min(self._nr_results, total_results)
        out = MetadataResult(total=total_results,
                             start=int(res.get('start', 0)),
                             pageLength=int(res.get('pageLength', 0)),
                             recordsRetrieved=nr_results)
        return out

    @property
    def records(self) -> list[MetadataRecord]:
        """Contains the individual records that matched the query.

        Returns:
            list[MetadataRecord]: List of MetadataRecord objects which contain the following
            items of a document: `contentType`, 
            `identifier`, `language`, `url`, `url_format`, `url_platform`, `title`, `creators`, 
            `publicationName`, `openaccess`, `doi`, `publisher`, `publicationDate`,
            `publicationType`, `issn`, `volume`, `number`, `genre`, `startingPage`, 
            `endingPage`, `journalId`, `copyright`, `abstract` and `subjects`.
        """
        records_list = []
        for record in self._json.get('records', []):
            url = record.get('url', {})[0].get('value')
            url_format = record.get('url', {})[0].get('format')
            url_platform = record.get('url', {})[0].get('platform')

            creators = []
            for ceator in record.get('creators', []):
                creators.append(MetadataCreator(creator=ceator.get('creator'),
                                                ORCID=ceator.get('ORCID')))

            records_list.append(
                MetadataRecord(
                    contentType=record.get('contentType'),
                    identifier=record.get('identifier'),
                    language=record.get('language'),
                    url=url,
                    url_format=url_format,
                    url_platform=url_platform,
                    title=record.get('title'),
                    creators=creators,
                    publicationName=record.get('publicationName'),
                    openaccess=str_to_bool(record.get('openaccess')),
                    doi=record.get('doi'),
                    publisher=record.get('publisher'),
                    publicationDate=record.get('publicationDate'),
                    publicationType=record.get('publicationType'),
                    issn=record.get('issn'),
                    volume=make_int_if_possible(record.get('volume')),
                    number=make_int_if_possible(record.get('number')),
                    genre=record.get('genre'),
                    startingPage=make_int_if_possible(record.get('startingPage')),
                    endingPage=make_int_if_possible(record.get('endingPage')),
                    journalId=make_int_if_possible(record.get('journalId')),
                    copyright=record.get('copyright'),
                    abstract=record.get('abstract'),
                    subjects=record.get('subjects')
                )
            )
        return records_list

    def __init__(self,
                 query: str = '',
                 start: int = 1,
                 nr_results: int = 10,
                 premium: bool = False,
                 cache: bool = True,
                 refresh: Union[bool, int] = False,
                 **kwargs):
        """
        Args:
            query (str): The query to search for.
            start (int): The starting index for the results. Defaults to 1.
            nr_results (int): The number of results to retrieve. Defaults to 10.
            premium (bool): Whether the user has a premium account. Defaults to False.
            cache (bool): Whether to cache the results. Defaults to True.
            refresh (bool|int): Weather to refresh the cache. If an integer is provided, 
                it will be used as the cache expiration time in days. Defaults to False.
            kwargs: Additional fields for query (e.g. issn, datefrom, dateto, etc.). For a comprehensive list of
                available fields, see the 
                `Springer Metadata API documentation <https://dev.springernature.com/docs/supported-query-params/>`_.

        This class is iterable, allowing you to iterate over the metadata `records` retrieved.
        It also supports indexing to access the metadata of specific documents.

        Example:
            Retrieve the metadata of documents with the word 'Segmentation' from the journal
            with the ISSN '1573-7497' starting from the date '2024-01-01'.
            

            >>> metadata = Metadata('Segmentation', issn='1573-7497', datefrom='2024-01-01')
            >>> for record in metadata:
            >>>     print(record)
     
        Note:
            The properties `facets`, `records` and `results` can be converted to a pandas 
            DataFrame with `pd.DataFrame(object.property)`.
        """
        api = self.__class__.__name__
        super().__init__(query=query,
                         api=api,
                         start=start,
                         nr_results=nr_results,
                         premium=premium,
                         cache=cache,
                         refresh=refresh,
                         **kwargs)
        self._nr_results = nr_results
        self._records = self.records

    def __iter__(self):
        return iter(self._records)

    def __getitem__(self, index):
        return self._records[index]

    def __len__(self):
        return len(self._records)

    def __repr__(self):
        return self._records.__repr__()
