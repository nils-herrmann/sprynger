"""Module with the chapter class for the OpenAccess class."""
from typing import Optional, Union

from sprynger.utils.data_structures import Affiliation, Contributor, Date, Paragraph
from sprynger.utils.parse import get_attr, get_text, make_int_if_possible
from sprynger.utils.parse_openaccess import (
    affs_to_dict,
    get_contributors,
    get_affiliations,
    get_date,
    get_paragraphs,
)

class Chapter:
    """Auxiliary class to parse a chapter from a book."""
    @property
    def affiliations(self) -> list[Affiliation]:
        """List of affiliations of the collaborators of the chapter. Each affiliation is represented
        as a named tuple with the following fields:
        `type`, `ref_nr`, `ror`, `grid`, `isni`, `division`, `name`, `city`, `country`.
        
        Note: To match affiliations with contributors use the affiliation's `ref_nr` and the
        contributor's `affiliations_ref_nr`.
        """
        return get_affiliations(self._data)

    @property
    def affiliations_dict(self) -> dict[str, Affiliation]:
        """Auxiliary property to query the affiliations by their reference number."""
        return affs_to_dict(self.affiliations)

    @property
    def contributors(self) -> list[Contributor]:
        """List of contributors of the chapter. Each contributor is represented as a named tuple
        with the following fields:
        `type`, `nr`, `orcid`, `surname`, `given_name`, `email`, `affiliations_ref_nr`.

        Note: To match contributors with affiliations use the contributor's `affiliations_ref_nr`
        and the affiliation's `ref_nr`.
        """
        return get_contributors(self._data)

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
    def date_epub(self) -> Date:
        """Electronic publication date of the chapter."""
        date_node = self._chapter_meta.find('.//pub-date[@publication-format="electronic"]')
        return get_date(date_node)

    @property
    def date_ppub(self) -> Date:
        """Print publication date of the chapter."""
        date_node = self._chapter_meta.find('.//pub-date[@publication-format="print"]')
        return get_date(date_node)

    @property
    def date_registration(self) -> Date:
        """Registration date of the chapter."""
        date_node = self._chapter_meta.find('.//pub-history/date[@date-type="registration"]')
        return get_date(date_node)

    @property
    def date_online(self) -> Date:
        """Online date of the chapter."""
        date_node = self._chapter_meta.find('.//pub-history/date[@date-type="online"]')
        return get_date(date_node)

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