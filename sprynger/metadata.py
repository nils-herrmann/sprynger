from typing import Optional, Literal
from pandas import DataFrame

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
            list[MetadataFacets]: A list of MetadataFacets objects containing the `facet`, `value`, and `count`.
        """
        facets_list = []
        for facet in self.json.get('facets'):
            facet_name = facet.get('name')
            for item in facet.get('values', []):
                new_facet = MetadataFacets(facet=facet_name,
                                           value=item.get('value'),
                                           count=item.get('count'))
                facets_list.append(new_facet)
        return facets_list

    @property
    def facets_df(self) -> DataFrame:
        """DataFrame with the facets of the results.

        Returns:
            pd.DataFrame: A DataFrame containing the `facets`, `values`, and `counts`.

        Example:
            >>> df = self.facets_df
            >>> print(df.head())
                 facet                                              value  count
            0    subject  Probability and Statistics in Computer Science   1816
            1    subject  Probability Theory and Stochastic Processes     1816
            2    subject  Statistics                                      1816
        """

        return DataFrame(self.facets)

    @property
    def results(self) -> dict:
        """Dictionary with an overview of the results of the query.

        Returns:
            dict: A dictionary containing the following keys the `total` matches found, `start` index of the first result, 
            `pageLength` number of results per page, `recordsDisplayed` number of records displayed.
        """
        res = self.json.get('result', [{}])
        return res[0]

    @property
    def records(self) -> list[MetadataRecord]:
        """Contains the individual records that matched the query.
        
        Returns:
            list: of MetadataRecord objects which contain the following items of a document: `contentType`, `identifier`, `language`, `url`, 
            `url_format`, `url_platform`, `title`, `creators`, `publicationName`, `openaccess`, `doi`, `publisher`, 
            `publicationDate`, `publicationType`, `issn`, `volume`, `number`, `genre`, `startingPage`, `endingPage`,
            `journalId`, `copyright`, `abstract` and `subjects`.
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
    
    @property
    def records_df(self) -> DataFrame:
        """Create a DataFrame where each row represents the metadata of a document.

        Returns:
            pd.DataFrame: A DataFrame containing the following columns: `contentType`, `identifier`, `language`, `url`, 
            `url_format`, `url_platform`, `title`, `creators`, `publicationName`, `openaccess`, `doi`, `publisher`, 
            `publicationDate`, `publicationType`, `issn`, `volume`, `number`, `genre`, `startingPage`, `endingPage`, 
            `journalId`, `copyright`, `abstract` and `subjects`.
        """
        return DataFrame(self.records)


    def __init__(self,
                 id: str,
                 id_type: Optional[Literal['doi', 'issn', 'isbn']] = None,
                 start: int = 1,
                 max_results: int = 10):
        """Initialize the Metadata object to retrieve metadata from the Springer Metadata API. Depending on the type of 
        identifier, the API will return either:
        - doi: One single article 
        - issn: All articles from a journal
        - isbn: All chapters from a book

        Args:
            id (str): The identifier of the article (doi) or the journal (issn) or book (isbn).
            id_type (Optional[Literal['doi', 'issn', 'isbn']]): The type of the identifier. If not provided, it will be detected automatically.
            start (int): The starting index for the results. Defaults to 1.
            max_results (int): The maximum number of results to retrieve. Defaults to 10.            
        """

        self._id = id
        self._id_type = id_type
        self._start = start
        self._max_results = max_results

        if self._id_type is None:
            self._id_type = detect_id_type(self._id)

        
        super().__init__(id=self._id,
                         id_type=self._id_type,
                         api='metadata',
                         start=self._start,
                         max_results=self._max_results)