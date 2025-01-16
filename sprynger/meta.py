"""
Module with Meta class.
"""
from typing import Union

from sprynger.metadata import Metadata
from sprynger.utils.data_structures import MetadataCreator, MetaDiscipline, MetaRecord, MetaURL
from sprynger.utils.parse import make_int_if_possible, str_to_bool


class Meta(Metadata):
    """Class to retreive the metadata of a document from the Springer Meta v2 API."""
    @property
    def records(self) -> list[MetaRecord]:
        """Contains the individual records that matched the query.

        Returns:
            list[MetaRecord]: List of MetaRecord objects which contain the following
            items of a document: `contentType`,
            `identifier`, `language`, `urls`, `title`, `creators`,
            `publicationName`, `openaccess`, `doi`, `publisher`, `publicationDate`,
            `publicationType`, `issn`, `eIssn`, `volume`, `number`, `issueType`,
            `topicalCollection`, `genre`, `startingPage`,
            `endingPage`, `journalId`, `onlineDate`,
            `copyright`, `abstract`, `conferenceInfo`, 
            `keyword`, `subjects` and `disciplines`.
        """
        def parse_urls(urls):
            return [MetaURL(format=url.get('format'), platform=url.get('platform'), value=url.get('value')) for url in urls]

        def parse_creators(creators):
            return [MetadataCreator(creator=creator.get('creator'), ORCID=creator.get('ORCID')) for creator in creators]

        def parse_disciplines(disciplines):
            return [MetaDiscipline(id=discipline.get('id'), term=discipline.get('term')) for discipline in disciplines]

        records_list = []
        for record in self._json.get('records', []):
            urls = parse_urls(record.get('url', []))
            creators = parse_creators(record.get('creators', []))
            disciplines = parse_disciplines(record.get('disciplines', []))

            records_list.append(
                MetaRecord(
                    contentType=record.get('contentType'),
                    identifier=record.get('identifier'),
                    language=record.get('language'),
                    urls=urls,
                    title=record.get('title'),
                    creators=creators,
                    publicationName=record.get('publicationName'),
                    openaccess=str_to_bool(record.get('openaccess')),
                    doi=record.get('doi'),
                    publisher=record.get('publisher'),
                    publicationDate=record.get('publicationDate'),
                    publicationType=record.get('publicationType'),
                    issn=record.get('issn'),
                    eIssn=record.get('eIssn'),
                    volume=make_int_if_possible(record.get('volume')),
                    number=make_int_if_possible(record.get('number')),
                    issueType=record.get('issueType'),
                    topicalCollection=record.get('topicalCollection'),
                    genre=record.get('genre'),
                    startingPage=make_int_if_possible(record.get('startingPage')),
                    endingPage=make_int_if_possible(record.get('endingPage')),
                    journalId=make_int_if_possible(record.get('journalId')),
                    onlineDate=record.get('onlineDate'),
                    copyright=record.get('copyright'),
                    abstract=record.get('abstract'),
                    conferenceInfo = record.get('conferenceInfo'),
                    keyword = record.get('keyword'),
                    subjects=record.get('subjects'),
                    disciplines=disciplines
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
            Retrieve the metadata of documents that match the query 'Segmentation' with ISSN '1573-7497' and
            starting from the date '2024-01-01'.
            
            >>> meta = Meta('Segmentation', issn='1573-7497', datefrom='2024-01-01')
            >>> for record in metadata:
            >>>     print(record)
     
        Note:
            The properties `facets`, `records` and `results` can be converted to a pandas
            DataFrame with `pd.DataFrame(object.property)`.
        """
        super().__init__(query=query,
                         start=start,
                         nr_results=nr_results,
                         premium=premium,
                         cache=cache,
                         refresh=refresh,
                         **kwargs)
        self._nr_results = nr_results
        self._records = self.records
