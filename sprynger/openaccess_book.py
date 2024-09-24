"""Module with two classes to retrieve data from Springer Books:

- **OpenAccessChapter:** class to retrieve a *single* chapter from Springer Open Access Books.
- **OpenAccessBook:** class to retrieve data and articles of a book (Single chapters can also be queried).
"""
from typing import Literal, Optional, Union

from sprynger.retrieve import Retrieve
from sprynger.utils.fetch import detect_id_type
from sprynger.utils.data_structures import (BookMeta,
                                            ChapterMeta,
                                            OpenAcessParagraph)
from sprynger.utils.parse import get_attr, get_text
from sprynger.utils.parse_openaccess import get_paragraphs


class _Chapter:
    """Auxiliary class to retrieve a chapter from a book."""
    @property
    def metadata(self) -> ChapterMeta:
        """Metadata of the book chapter(s).
        
        Returns:
            ChapterMeta: A list of ChapterMeta objects containing the `doi` and `chapter`.
        """
        doi, chapter = None, None
        metadata  =  self._data.find('.//book-part-meta')
        if metadata is not None:
            doi = get_attr(metadata, 'book-part-id', 'book-part-id-type', 'doi')
            chapter = get_attr(metadata, 'book-part-id', 'book-part-id-type', 'chapter')

        chapter_data = ChapterMeta(doi=doi,
                                   chapter=chapter)

        return chapter_data

    @property
    def paragraphs(self) -> list[OpenAcessParagraph]:
        """Paragraphs of the book chapter.
        
        Returns:
            list[OpenAcessParagraph]: A list of OpenAcessParagraph objects containing the
            `paragraph_id`, `section_id`, `section_title`, and `text`.
        """
        return get_paragraphs(self._data)


    def __init__(self, data):
        self._data = data

class OpenAccessBook(Retrieve):
    """Retrieve an Open Access book from Springer Nature API."""
    @property
    def metadata(self) -> BookMeta:
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

    def __init__(self,
                identifier: str,
                id_type: Optional[Literal['doi', 'isbn']] = None,
                start: int = 1,
                nr_results: int = 10,
                premium: bool = False,
                cache: bool = True,
                refresh: Union[bool, int] = False):
        """
        Args:
            identifier (str): Identifier of the book (ISBN or DOI).
                Providing a DOI *of a chapter* will return a single chapter.
            id_type (Optional[Literal['doi', 'isbn']], optional): Type of the identifier
              Defaults to None.
            start (int, optional): Start index of the results. Defaults to 1.
            nr_results (int): The number of results to retrieve. Defaults to 10.
            premium (bool): Whether the user has a premium account. Defaults to False.
            cache (bool): Whether to cache the results. Defaults to True.
            refresh (bool|int): Weather to refresh the cache. If an integer is provided, 
                it will be used as the cache expiration time in days. Defaults to False.
        
        This class is iterable, allowing the user to iterate over the chapters of the book.
        It also allows the user to access the chapters by index.

        Example:
            >>> book = OpenAccessBook(doi='10.1007/978-3-030-43582-0')
            >>> print(book.metadata)
            >>> for chapter in book.chapters:
            >>>     print(chapter.title)


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
                        api='OpenAccessBook',
                        start=self._start,
                        nr_results=self._nr_results,
                        premium=premium,
                        cache=cache,
                        refresh=refresh)

        self.chapters = self._get_chapters()

    def _get_chapters(self) -> list[_Chapter]:
        """Auxiliary function to get the chapters from the XML data."""
        chapters = []
        for chapter_data in self.xml.findall('.//book-part[@book-part-type="chapter"]'):
            chapter = _Chapter(chapter_data)
            chapters.append(chapter)
        return chapters

    def __iter__(self):
        return iter(self.chapters)

    def __getitem__(self, index):
        return self.chapters[index]

    def __len__(self):
        return len(self.chapters)


class OpenAccessChapter(_Chapter):
    """Retrieve an Open Access chapter from Springer Nature API."""
    @property
    def book_metadata(self):
        """Metadata of the book.

        Returns:
            BookMeta: A BookMeta object containing the `doi`, `publisher_id`, `book_title_id`,
        """
        return self._book_object.metadata

    @property
    def metadata(self):
        return self._chapter_object.metadata

    @property
    def paragraphs(self):
        return self._chapter_object.paragraphs

    def __init__(self,
                 doi: str,
                 cache: bool = True,
                 refresh: Union[bool, int] = False):
        """
        Args:
            doi (str): DOI of the chapter.
            cache (bool, optional): Cache the data. Defaults to True.
            refresh (Union[bool, int], optional): Refresh the cache. Defaults to False.
        """
        self._book_object = OpenAccessBook(identifier=doi,
                                           id_type='doi',
                                           start=1,
                                           nr_results=1,
                                           cache=cache,
                                           refresh=refresh)
        self._chapter_object = self._book_object.chapters[0]
