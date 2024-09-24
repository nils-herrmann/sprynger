"""Module with two classes to retrieve data from Springer Journals:

- **OpenAccessArticle:** class to retrieve a *single* article from Springer Open Access Journals.
- **OpenAccessJournal:** class to retrieve data and articles of a journal (Single articles can also be queried).
"""
from typing import Literal, Optional, Union

from sprynger.retrieve import Retrieve
from sprynger.utils.fetch import detect_id_type

from sprynger.utils.data_structures import (ArticleMeta, JournalMeta, OpenAcessParagraph)
from sprynger.utils.parse import get_attr, get_text
from sprynger.utils.parse_openaccess import get_paragraphs

class _Article:
    @property
    def metadata(self) -> ArticleMeta:
        """Metadata of an article.
        
        Returns:
            ArticleMeta: ArticleMeta objects containing the `article_type`, `language`,
            `publisher_id`, `manuscript`, and `doi`.
        """
        article_type = self._data.get('article-type')
        language = self._data.get('{http://www.w3.org/XML/1998/namespace}lang')

        publisher_id, manuscript, doi = None, None, None
        metadata  =  self._data.find('.//front/article-meta')
        if metadata is not None:
            publisher_id = get_attr(metadata, 'article-id', 'pub-id-type', 'publisher-id')
            manuscript = get_attr(metadata, 'article-id', 'pub-id-type', 'manuscript')
            doi = get_attr(metadata, 'article-id', 'pub-id-type', 'doi')

        data = ArticleMeta(article_type=article_type,
                            language=language,
                            publisher_id=publisher_id,
                            manuscript=manuscript,
                            doi=doi)
        return data

    @property
    def paragraphs(self) -> list[OpenAcessParagraph]:
        """Paragraphs of the article.

        Returns:
            list[OpenAcessParagraph]: A list of OpenAcessParagraph objects containing the 
            `paragraph_id`, `section_id`, `section_title`, and `text`.
        """
        return get_paragraphs(self._data)

    def __init__(self, data):
        self._data = data

class OpenAccessJournal(Retrieve):
    """Retrieve an Open Access journal from Springer Nature API."""
    @property
    def metadata(self) -> JournalMeta:
        """Metadata of the journal.
        
        Returns:
            JournalMeta: JournalMeta objects containing the `publisher_id`, `doi`, `journal_title`,
            `journal_abbrev_title`, `issn_print`, `issn_electronic`, `publisher_name`,
            and `publisher_loc`.
        """
        publisher_id, doi, journal_title = None, None, None
        journal_abbrev_title, issn_print, issn_electronic = None, None, None
        publisher_name, publisher_loc = None, None

        metadata = self.xml.find('.//journal-meta')
        if metadata is not None:
            publisher_id = get_attr(metadata, 'journal-id', 'journal-id-type', 'publisher-id')
            doi = get_attr(metadata, 'journal-id', 'journal-id-type', 'doi')
            journal_title = get_text(metadata, './/journal-title')
            journal_abbrev_title = get_text(metadata, './/abbrev-journal-title')
            issn_print = get_attr(metadata, 'issn', 'pub-type', 'ppub')
            issn_electronic = get_attr(metadata, 'issn', 'pub-type', 'epub')
            publisher_name = get_text(metadata, './/publisher-name')
            publisher_loc = get_text(metadata, './/publisher-loc')

        journal_metadata = JournalMeta(publisher_id=publisher_id,
                            doi=doi,
                            journal_title=journal_title,
                            journal_abbrev_title=journal_abbrev_title,
                            issn_print=issn_print,
                            issn_electronic=issn_electronic,
                            publisher_name=publisher_name,
                            publisher_loc=publisher_loc)

        return journal_metadata


    def __init__(self,
                identifier: str,
                id_type: Optional[Literal['doi', 'issn']] = None,
                start: int = 1,
                nr_results: int = 10,
                premium: bool = False,
                cache: bool = True,
                refresh: Union[bool, int] = False):
        """
        Args:
            identifier (str): The identifier of the journal (ISSN).
                Providing a DOI will return just one article.
            id_type (Optional[Literal['doi', 'issn']]): The type of the identifier.
                If not provided, it will be detected automatically.
            start (int): The starting index for the results. Defaults to 1.
            nr_results (int): The number of results to retrieve. Defaults to 10.
            premium (bool): Whether the user has a premium account. Defaults to False.
            cache (bool): Whether to cache the results. Defaults to True.
            refresh (bool|int): Weather to refresh the cache. If an integer is provided, 
                it will be used as the cache expiration time in days. Defaults to False.

        This class is iterable, allowing you to iterate over the articles retrieved 
        from the journal.
        It also supports indexing to access specific articles.

        Example:
            >>> journal = OpenAccessJournal(identifier='some-issn')
            >>> for article in journal:
            >>>     print(article.metadata)
            >>> first_article = journal[0]
        """
        self._id = identifier
        self._id_type = id_type
        self._start = start
        self._nr_results = nr_results

        # Detect the identifier type if not provided
        if self._id_type is None:
            self._id_type = detect_id_type(self._id)

        super().__init__(identifier=self._id,
                        id_type=self._id_type,
                        api='OpenAccessJournal',
                        start=self._start,
                        nr_results=self._nr_results,
                        premium=premium,
                        cache=cache,
                        refresh=refresh)

        self.articles = self._get_articles()

    def _get_articles(self) -> list[_Article]:
        """Auxiliary function to get the articles from the XML data."""
        articles = []
        for article_data in self.xml.findall('.//article'):
            article = _Article(article_data)
            articles.append(article)
        return articles

    def __iter__(self):
        return iter(self.articles)

    def __getitem__(self, index):
        return self.articles[index]

    def __len__(self):
        return len(self.articles)


class OpenAccessArticle(_Article):
    """Retrieve an Open Access article from Springer Nature API."""
    @property
    def journal_metadata(self):
        """Metadata of the journal.
        
        Returns:
            JournalMeta: JournalMeta objects containing the 
            `publisher_id`, `doi`, `journal_title`, `journal_abbrev_title`, `issn_print`, 
            `issn_electronic`, `publisher_name`, and `publisher_loc`.
        """
        return self._journal_object.metadata

    @property
    def metadata(self):
        return self._article_object.metadata

    @property
    def paragraphs(self):
        return self._article_object.paragraphs

    def __init__(self,
                 doi: str,
                 cache: bool = True,
                 refresh: Union[bool, int] = False):
        """
        Args:
            doi (str): Digital Object Identifier (DOI) of the article.
            cache (bool, optional): Whether to cache the data. Defaults to True.
            refresh (Union[bool, int], optional): Whether to refresh the cache. 
                If int, it specifies the number of days after which the cache should be refreshed. 
                Defaults to False.
        """
        self._journal_object = OpenAccessJournal(identifier=doi,
                                         id_type='doi',
                                         start=1,
                                         nr_results=1,
                                         cache=cache,
                                         refresh=refresh)
        self._article_object = self._journal_object.articles[0]
