"""Module with two classes to retrieve data from the Springer Nature OpenAccess API. Depending 
on the type of data to retrieve, the user can use:

- `OpenAccessJournal`: class to retrieve data of a journal. Single articles can also be queried.
- `OpenAccessBook`: class to retrieve data of a book. Single chapters can also be queried.
"""
from typing import Literal, Optional, Union

from sprynger.openaccess_base import OpenAccessBase
from sprynger.utils.data_structures import (ArticleMeta, BookMeta,
                                            ChapterMeta, JournalMeta,
                                            OpenAcessParagraph)
from sprynger.utils.parse import get_attr, get_text

class OpenAccessJournal(OpenAccessBase):
    """Class to retrieve journal/article data from the Springer OpenAccess API."""
    @property
    def article_meta(self) -> list[ArticleMeta]:
        """Metadata of the article(s).
        
        Returns:
            list[ArticleMeta]: A list of ArticleMeta objects containing the 
            `publisher_id`, `manuscript`, and `doi`.
        """
        articles_metadata = []
        for document in self.xml.findall('.//article'):

            publisher_id, manuscript, doi = None, None, None
            metadata  =  document.find('.//article-meta')
            if metadata is not None:
                publisher_id = get_attr(metadata, 'article-id', 'pub-id-type', 'publisher-id')
                manuscript = get_attr(metadata, 'article-id', 'pub-id-type', 'manuscript')
                doi = get_attr(metadata, 'article-id', 'pub-id-type', 'doi')

            data = ArticleMeta(publisher_id=publisher_id,
                               manuscript=manuscript,
                               doi=doi)
            articles_metadata.append(data)

        return articles_metadata
    
    @property
    def journal_meta(self) -> JournalMeta:
        """Metadata of the journal.
        
        Returns:
            list[JournalMeta]: A list of JournalMeta objects containing the 
            `publisher_id`, `doi`, `journal_title`, `journal_abbrev_title`, `issn_print`, 
            `issn_electronic`, `publisher_name`, and `publisher_loc`.
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


    @property
    def paragraphs(self) -> list[list[OpenAcessParagraph]]:
        """Paragraphs of the article(s). This property returns a list of the paragraphs *for each article*.
        The paragraphs of an article are in form of a list of OpenAcessParagraph named tuples.

        Returns:
            list[list[OpenAcessParagraph]]: A list of OpenAcessParagraph objects containing the 
            `paragraph_id`, `section_id`, `section_title`, and `text`.
        """
        return super().get_paragraphs(document_type='article')

    def __init__(self,
                identifier: str,
                id_type: Optional[Literal['doi', 'issn']] = None,
                start: int = 1,
                max_results: int = 10,
                cache: bool = True,
                refresh: Union[bool, int] = False):
        """Retrieve journal/articles data from the Springer OpenAccess API. 
        Depending on the type of identifier, the API will return either:
        - doi: One single article 
        - issn: All articles from a journal

        Args:
            identifier (str): The identifier of the article (doi) or the journal (issn).
            id_type (Optional[Literal['doi', 'issn']]): The type of the identifier.
                If not provided, it will be detected automatically.
            start (int): The starting index for the results. Defaults to 1.
            max_results (int): The maximum number of results to retrieve. Defaults to 10.
            cache (bool): Whether to cache the results. Defaults to True.
            refresh (bool|int): Weather to refresh the cache. If an integer is provided, 
                it will be used as the cache expiration time in days. Defaults to False.
        
        Note:
            - For books/chapters use the `OpenAccessBooks` class.
            - All properties can be converted to a pandas 
                DataFrame with `pd.DataFrame(object.property)`.
        """
        super().__init__(identifier=identifier, id_type=id_type,
                         start=start, max_results=max_results,
                         cache=cache, refresh=refresh)
        self._document_type = 'article'


class OpenAccessBook(OpenAccessBase):
    """Class to retrieve data from a book/chapter from the Springer OpenAccess API."""
    @property
    def book_meta(self) -> BookMeta:
        """Metadata of the book.
        
        Returns:
            BookMeta: A BookMeta object containing the `doi`, `publisher_id`, `book_title_id`, 
            `pub_date`, `isbn_print`, `isbn_electronic`, `publisher_name`, and `publisher_loc`.
            
        """
        doi, publisher_id, book_title_id = None, None, None
        pub_date, isbn_print, isbn_electronic = None, None, None
        publisher_name, publisher_loc = None, None

        metadata = self.xml.find('.//book-meta')
        if metadata is not None:
            doi = get_attr(metadata, 'book-id', 'book-id-type', 'doi')
            publisher_id = get_attr(metadata, 'book-id', 'book-id-type', 'publisher-id')
            book_title_id = get_attr(metadata, 'book-id', 'book-id-type', 'book-title-id')
            pub_date = get_text(metadata, './/pub-date[@date-type="pub"]/string-date')
            isbn_print = get_attr(metadata, 'isbn', 'content-type', 'ppub')
            isbn_electronic = get_attr(metadata, 'isbn', 'content-type', 'epub')
            publisher_name = get_text(metadata, './/publisher/publisher-name')
            publisher_loc = get_text(metadata, './/publisher/publisher-loc')

        metadata = BookMeta(doi=doi,
                            publisher_id=publisher_id,
                            book_title_id=book_title_id,
                            pub_date=pub_date,
                            isbn_print=isbn_print,
                            isbn_electronic=isbn_electronic,
                            publisher_name=publisher_name,
                            publisher_loc=publisher_loc)


        return metadata

    @property
    def chapter_meta(self) -> list[ArticleMeta]:
        """Metadata of the book chapter(s).
        
        Returns:
            list[ChapterMeta]: A list of BookMeta objects containing the 
            `doi`, `publisher_id`, and `book_title_id`.
        """
        chapters_metadata = []
        for document in self.xml.findall('.//book-part'):

            doi, chapter = None, None
            metadata  =  document.find('.//book-part-meta')
            if metadata is not None:
                doi = get_attr(metadata, 'book-part-id', 'book-part-id-type', 'doi')
                chapter = get_attr(metadata, 'book-part-id', 'book-part-id-type', 'chapter')

            data = ChapterMeta(doi=doi,
                               chapter=chapter)
            chapters_metadata.append(data)

        return chapters_metadata

    @property
    def paragraphs(self) -> list[list[OpenAcessParagraph]]:
        """Paragraphs of the chapter(s). This property returns a list of the 
        paragraphs *for each chapter*. The paragraphs of a chapter are in form of a 
        list of OpenAcessParagraph named tuples.

        Returns:
            list[list[OpenAcessParagraph]]: A list of OpenAcessParagraph objects containing the 
            `paragraph_id`, `section_id`, `section_title`, and `text`.
        """
        return super().get_paragraphs(document_type='book-part')

    def __init__(self,
                identifier: str,
                id_type: Optional[Literal['doi','isbn']] = None,
                start: int = 1,
                max_results: int = 10,
                cache: bool = True,
                refresh: Union[bool, int] = False):
        """Retrieve book/chapters from the Springer OpenAccess API. 
        Depending on the type of identifier, the API will return either:
        - doi: One single chapter 
        - isbn: All chapters from a book

        Args:
            identifier (str): The identifier of the chapter (doi) or book (isbn).
            id_type (Optional[Literal['doi', 'isbn']]): The type of the identifier. If 
                not provided, it will be detected automatically.
            start (int): The starting index for the results. Defaults to 1.
            max_results (int): The maximum number of results to retrieve. Defaults to 10.
            cache (bool): Whether to cache the results. Defaults to True.
            refresh (bool|int): Weather to refresh the cache. If an integer is provided, 
                it will be used as the cache expiration time in days. Defaults to False.
        
        Note:
            - For journals/articles use the `OpenAccessJournal` class.
            - All properties can be converted to a pandas DataFrame
                with `pd.DataFrame(object.property)`.
        """
        super().__init__(identifier=identifier, id_type=id_type,
                         start=start, max_results=max_results,
                         cache=cache, refresh=refresh)
