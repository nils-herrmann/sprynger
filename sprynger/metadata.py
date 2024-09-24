"""There are two classes in this module:

- **DocumentMetadata:** Retrieve the metadata of a *single* document from the Springer Metadata API.
- **Metadata:** Retrieve the metadata of a documents associated with a journal or book from the Springer Metadata API.
"""
from typing import Literal, Optional, Union

from sprynger.retrieve import Retrieve
from sprynger.utils.fetch import detect_id_type
from sprynger.utils.data_structures import MetadataCreator, MetadataFacets, MetadataRecord, MetadataResult
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
    def results(self) -> MetadataResult:
        """Overview of the results of the query.

        Returns:
            MetadataResult: An object containing the the `total` matches found, `start` 
            index of the first result, max `pageLength` when paginating and the number of 
            `recordsRetrieved`.
        """
        res = self.json.get('result', [{}])[0]
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
                 nr_results: int = 10,
                 premium: bool = False,
                 cache: bool = True,
                 refresh: Union[bool, int] = False):
        """
        Args:
            identifier (str): The identifier of the article (doi) 
                or the journal (issn) or book (isbn).
            id_type (Optional[Literal['doi', 'issn', 'isbn']]): The type of the identifier.
                If not provided, it will be detected automatically.
            start (int): The starting index for the results. Defaults to 1.
            nr_results (int): The number of results to retrieve. Defaults to 10.
            premium (bool): Whether the user has a premium account. Defaults to False.
            cache (bool): Whether to cache the results. Defaults to True.
            refresh (bool|int): Weather to refresh the cache. If an integer is provided, 
                it will be used as the cache expiration time in days. Defaults to False.

        This class is iterable, allowing you to iterate over the metadata `records` retrieved.
        It also supports indexing to access the metadata of specific documents.

        Example:
            >>> metadata = Metadata('id-book-or-journal')
            >>> for record in metadata:
            >>>     print(record)
     
        Note:
            - All properties can be converted to a pandas DataFrame with `pd.DataFrame(object.property)`.

        """

        self._id = identifier
        self._id_type = id_type
        self._start = start
        self._nr_results = nr_results

        if self._id_type is None:
            self._id_type = detect_id_type(self._id)

        super().__init__(identifier=self._id,
                         id_type=self._id_type,
                         api='Metadata',
                         start=self._start,
                         nr_results=self._nr_results,
                         premium=premium,
                         cache=cache,
                         refresh=refresh)
        self._records = self.records

    def __iter__(self):
        return iter(self._records)

    def __getitem__(self, index):
        return self._records[index]

    def __len__(self):
        return len(self._records)


class DocumentMetadata(Metadata):
    """Class to retrieve the metadata of a *single* document from the Springer Metadata API."""
    @property
    def metadata(self) -> MetadataRecord:
        """The metadata of a document.

        Returns:
            MetadataRecord: A MetadataRecord object containing the metadata of the document.
            This object contains the following items: `contentType`, 
            `identifier`, `language`, `url`, `url_format`, `url_platform`, `title`, `creators`, 
            `publicationName`, `openaccess`, `doi`, `publisher`, `publicationDate`,
            `publicationType`, `issn`, `volume`, `number`, `genre`, `startingPage`, 
            `endingPage`, `journalId`, `copyright`, `abstract` and `subjects`.
        """
        return self.records[0]

    def __init__(self,
                 doi: str,
                 cache: bool = True,
                 refresh: Union[bool, int] = False):
        """Retrieve a **single** document metadata from the Springer Metadata API.

        Args:
            doi (str): The DOI of the document.
            cache (bool): Whether to cache the results. Defaults to True.
            refresh (bool|int): Weather to refresh the cache. If an integer is provided, 
                it will be used as the cache expiration time in days. Defaults to False.
        Note:
            To retrieve the metadata of all the documents in a book or journal, use the Metadata class.
        """

        super().__init__(identifier=doi,
                       id_type='doi',
                       start=1,
                       nr_results=1,
                       cache=cache,
                       refresh=refresh)
