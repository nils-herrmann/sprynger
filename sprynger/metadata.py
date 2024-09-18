"""Module with the Metadata class."""
from typing import Literal, Optional, Union

from sprynger.retrieve import Retrieve
from sprynger.utils.fetch import detect_id_type
from sprynger.utils.data_structures import MetadataCreator, MetadataFacets, MetadataRecord
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
        factets = self.json.get('facets', [])
        for facet in factets:
            facet_name = facet.get('name')
            for item in facet.get('values', []):
                new_facet = MetadataFacets(facet=facet_name,
                                           value=item.get('value'),
                                           count=item.get('count'))
                facets_list.append(new_facet)
        return facets_list

    @property
    def results(self) -> dict:
        """Dictionary with an overview of the results of the query.

        Returns:
            dict: A dictionary containing the following keys the `total` matches found, `start` 
            index of the first result, `pageLength` number of results per page, `recordsDisplayed` 
            number of records displayed.
        """
        res = self.json.get('result', [{}])
        return res[0]

    @property
    def records(self) -> list[MetadataRecord]:
        """Contains the individual records that matched the query.

        Returns:
            list: List of MetadataRecord objects which contain the following items of a 
            document: `contentType`, 
            `identifier`, `language`, `url`, `url_format`, `url_platform`, `title`, `creators`, 
            `publicationName`, `openaccess`, `doi`, `publisher`, `publicationDate`,
            `publicationType`, `issn`, `volume`, `number`, `genre`, `startingPage`, 
            `endingPage`,`journalId`, `copyright`, `abstract` and `subjects`.
        """
        records_list = []
        for record in self.json.get('records', []):
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
                 identifier: str,
                 id_type: Optional[Literal['doi', 'issn', 'isbn']] = None,
                 start: int = 1,
                 max_results: int = 10,
                 cache: bool = True,
                 refresh: Union[bool, int] = False):
        """Initialize the Metadata object to retrieve metadata from the Springer Metadata API. 
        Depending on the type of identifier, the API will return either:

        - doi: One single article 
        - issn: All articles from a journal
        - isbn: All chapters from a book

        Args:
            identifier (str): The identifier of the article (doi) 
                or the journal (issn) or book (isbn).
            id_type (Optional[Literal['doi', 'issn', 'isbn']]): The type of the identifier.
                If not provided, it will be detected automatically.
            start (int): The starting index for the results. Defaults to 1.
            max_results (int): The maximum number of results to retrieve. Defaults to 10.
            cache (bool): Whether to cache the results. Defaults to True.
            refresh (bool|int): Weather to refresh the cache. If an integer is provided, 
                it will be used as the cache expiration time in days. Defaults to False.

        Note:
            - All properties can be converted to a pandas DataFrame 
                with `pd.DataFrame(object.property)`.          
        """

        self._id = identifier
        self._id_type = id_type
        self._start = start
        self._max_results = max_results

        if self._id_type is None:
            self._id_type = detect_id_type(self._id)

        super().__init__(identifier=self._id,
                         id_type=self._id_type,
                         api='Metadata',
                         start=self._start,
                         max_results=self._max_results,
                         cache=cache,
                         refresh=refresh)
