"""
Module with the OpenAccess class to retrieve Open Access documents from Springer Nature API.
Iterate or slice the OpenAccess object to get the documents. Documents can be either:

- Articles: OpenAccess articles from journals.
- Chapters: OpenAccess chapters from books.

The OpenAccess class enables two options for full-text retrieval:

1. Use the `full_text` property to get the full text of the document in XML (JATS) format.
2. Use the `parsed_text` property to get the full text of the document parsed into sections.

Example:
    >>> from sprynger import OpenAccess
    >>> oa = OpenAccess('"Gaussian-mixture models"', datefrom='2024-01-01')
    >>> # Print doi and access the full text of the document
    >>> for doc in oa:
    >>>     print(doc.doi)
    >>>     print(doc.full_text)
    >>>     print(doc.parsed_text)



"""
from typing import Union

from sprynger.retrieve import Retrieve
from sprynger.openaccess_article import Article
from sprynger.openaccess_chapter import Chapter


class OpenAccess(Retrieve):
    """Retrieve Open Access documents from Springer Nature API."""
    @property
    def documents_found(self) -> int:
        """Number of documents found."""
        return self._get_total_results()

    def _get_documents(self) -> list[Union[Chapter, Article]]:
        """Auxiliary method to retrieve the documents from the Open Access API."""
        documents = []
        for record in self._xml.find('.//records'):
            if record.tag == 'book-part-wrapper':
                documents.append(Chapter(record))
            elif record.tag == 'article':
                documents.append(Article(record))
            else:
                raise ValueError(f'Unknown document type: {record.tag}')
        return documents

    @property
    def xml(self) -> str:
        """Raw XML response from the Open Access API."""
        return self._xml

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
            **kwargs: Additional fields for query (e.g. issn, datefrom, dateto, etc.).
                For a comprehensive list of available fields, see the 
                `Springer Metadata API documentation <https://dev.springernature.com/docs/supported-query-params/>`_.
        
        Example:
            Retrieve Open Access articles from the journal with ISSN '2223-7704' published after 
            '2024-01-01'.

            >>> oa = OpenAccess(issn=2223-7704, datefrom='2024-01-01')
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
