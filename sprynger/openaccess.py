"""
Module with the OpenAccess class to retrieve Open Access documents from Springer Nature API.
Iterate or slice the OpenAccess object to get the documents. Documents can be either:

- Articles: OpenAccess articles from journals.
- Chapters: OpenAccess chapters from books.

Example:
    >>> oa = OpenAccess('Eigenvalues', datefrom='2024-01-01')
    >>> for doc in oa:
    >>>     print(doc)
"""
from typing import Optional, Union

from sprynger.retrieve import Retrieve
from sprynger.utils.data_structures import Paragraph
from sprynger.utils.parse import get_attr, get_text, make_int_if_possible
from sprynger.utils.parse_openaccess import get_paragraphs

class Article:
    """Auxiliary class to parse an article from a journal."""
    @property
    def article_type(self) -> Optional[str]:
        """Type of the article."""
        return self._data.get('article-type')

    @property
    def doi(self) -> Optional[str]:
        """DOI of the article."""
        return get_attr(self._article_meta, 'article-id', 'pub-id-type', 'doi')

    @property
    def issn_electronic(self) -> Optional[str]:
        """Electronic ISSN of the journal."""
        return get_attr(self._journal_meta, 'issn', 'pub-type', 'epub')

    @property
    def issn_print(self) -> Optional[str]:
        """Print ISSN of the journal."""
        return get_attr(self._journal_meta, 'issn', 'pub-type', 'ppub')

    @property
    def journal_abbrev_title(self) -> Optional[str]:
        """Abbreviated title of the journal."""
        return get_text(self._journal_meta, './/abbrev-journal-title')

    @property
    def journal_doi(self) -> Optional[str]:
        """DOI of the journal."""
        return get_attr(self._journal_meta, 'journal-id', 'journal-id-type', 'doi')

    @property
    def journal_publisher_id(self) -> Optional[str]:
        """Publisher ID of the journal."""
        return get_attr(self._journal_meta, 'journal-id', 'journal-id-type', 'publisher-id')

    @property
    def journal_title(self) -> Optional[str]:
        """Title of the journal."""
        return get_text(self._journal_meta, './/journal-title')

    @property
    def language(self) -> Optional[str]:
        """Language of the article."""
        return self._data.get('{http://www.w3.org/XML/1998/namespace}lang')

    @property
    def manuscript(self) -> Optional[str]:
        """Manuscript of the article."""
        return get_attr(self._article_meta, 'article-id', 'pub-id-type', 'manuscript')

    @property
    def paragraphs(self) -> list[Paragraph]:
        """Paragraphs of the article.

        Returns:
            list[Paragraph]: A list of Paragraph objects containing the
            `paragraph_id`, `section_id`, `section_title`, and `text`.
        """
        return get_paragraphs(self._data)

    @property
    def publisher_id(self) -> Optional[str]:
        """Publisher ID of the article."""
        return get_attr(self._article_meta, 'article-id', 'pub-id-type', 'publisher-id')

    @property
    def publisher_loc(self) -> Optional[str]:
        """Location of the publisher."""
        return get_text(self._journal_meta, './/publisher-loc')

    @property
    def publisher_name(self) -> Optional[str]:
        """Name of the publisher."""
        return get_text(self._journal_meta, './/publisher-name')

    @property
    def title(self) -> Optional[str]:
        """Title of the article."""
        return get_text(self._article_meta, './/title-group/article-title')

    def __init__(self, data):
        self._data = data
        self._journal_meta = data.find('.//front/journal-meta')
        self._article_meta = data.find('.//front/article-meta')

    def __repr__(self) -> str:
        return f'Article {self.doi}'



class Chapter:
    """Auxiliary class to parse a chapter from a book."""
    @property
    def book_doi(self) -> Optional[str]:
        """DOI of the book."""
        return get_attr(self._book_meta, 'book-id', 'book-id-type', 'doi')

    @property
    def book_pub_date(self) -> Optional[str]:
        """Publication date of the book."""
        return get_text(self._book_meta, './/pub-date[@date-type="pub"]/string-date')

    @property
    def book_title(self) -> Optional[str]:
        """Title of the book."""
        return get_text(self._book_meta, './/book-title-group/book-title')

    @property
    def book_title_id(self) -> Optional[str]:
        """Book title ID."""
        return get_attr(self._book_meta, 'book-id', 'book-id-type', 'book-title-id')

    @property
    def book_sub_title(self) -> Optional[str]:
        """Sub-title of the book."""
        return get_text(self._book_meta, './/book-title-group/subtitle')

    @property
    def chapter_nr(self) -> Optional[Union[int, str]]:
        """Book chapter name or number."""
        chapter_nr = get_attr(self._chapter_meta, 'book-part-id', 'book-part-id-type', 'chapter')
        return make_int_if_possible(chapter_nr)

    @property
    def doi(self) -> Optional[str]:
        """DOI of the chapter."""
        doi = get_attr(self._chapter_meta, 'book-part-id', 'book-part-id-type', 'doi')
        return doi

    @property
    def isbn_electronic(self) -> Optional[str]:
        """ISBN of the electronic version of the book."""
        return get_attr(self._book_meta, 'isbn', 'content-type', 'epub')

    @property
    def isbn_print(self) -> Optional[str]:
        """ISBN of the print version of the book."""
        return get_attr(self._book_meta, 'isbn', 'content-type', 'ppub')

    @property
    def paragraphs(self) -> list[Paragraph]:
        """Paragraphs of the book chapter.
        
        Returns:
            list[Paragraph]: A list of Paragraph objects containing the
            `paragraph_id`, `section_id`, `section_title`, and `text`.
        """
        return get_paragraphs(self._data)

    @property
    def publisher_id(self) -> Optional[str]:
        """Publisher ID of the chapter's book."""
        return get_attr(self._book_meta, 'book-id', 'book-id-type', 'publisher-id')

    @property
    def publisher_loc(self) -> Optional[str]:
        """Location of the publisher."""
        return get_text(self._book_meta, './/publisher/publisher-loc')

    @property
    def publisher_name(self) -> Optional[str]:
        """Name of the publisher."""
        return get_text(self._book_meta, './/publisher/publisher-name')

    @property
    def title(self) -> Optional[str]:
        """Title of the chapter."""
        return get_text(self._chapter_meta, './/title-group/title')

    def __init__(self, data):
        self._data = data
        self._book_meta = data.find('.//book-meta')
        self._chapter_meta = data.find('.//book-part[@book-part-type="chapter"]/book-part-meta')


    def __repr__(self) -> str:
        return f'Chapter {self.doi}'


class OpenAccess(Retrieve):
    """Retrieve Open Access documents from Springer Nature API."""
    @property
    def documents_found(self) -> int:
        """Number of documents found."""
        return self._get_total_results()

    def _get_documents(self) -> list[Union[Chapter, Article]]:
        """Auciliary method to retrieve the documents from the Open Access API."""
        documents = []
        for record in self.xml.find('.//records'):
            if record.tag == 'book-part-wrapper':
                documents.append(Chapter(record))
            elif record.tag == 'article':
                documents.append(Article(record))
            else:
                raise ValueError(f'Unknown document type: {record.tag}')
        return documents

    def __init__(
        self,
        query: str = '',
        start: int = 1,
        nr_results: int = 10,
        premium: bool = False,
        cache: bool = True,
        refresh: Union[bool, int] = False,
        **kwargs,
    ) -> None:
        """
        Args:
            query (str): Query string.
            start (int): Start index of the results.
            nr_results (int): Number of results to retrieve.
            premium (bool): Use the premium API.
            cache (bool): Use the cache.
            refresh (Union[bool, int]): Refresh the cache.
            **kwargs: Additional fields to query.
        
        Example:
            >>> oa = OpenAccess(issn=2223-7704, datefrom='2024-01-01')
        
        Note:
            Check the Springer Nature API `documentation <http://docs-dev.springernature.com/docs/#querying-api/querying-api>`_ for the available fields.
        """

        super().__init__(query=query,
                         api='OpenAccess',
                         start=start,
                         nr_results=nr_results,
                         premium=premium,
                         cache=cache,
                         refresh=refresh,
                         **kwargs)
        self.documents = self._get_documents()

    def __iter__(self):
        return iter(self.documents)

    def __getitem__(self, index):
        return self.documents[index]

    def __len__(self):
        return len(self.documents)

    def __repr__(self):
        return self.documents.__repr__()
