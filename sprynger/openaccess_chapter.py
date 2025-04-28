"""Module with the chapter class for the OpenAccess class."""
from typing import Optional, Union

from lxml import etree

from sprynger.utils.data_structures import Affiliation, Contributor, Date, Reference, Section
from sprynger.utils.parse import get_attr, get_text, make_int_if_possible
from sprynger.utils.parse_openaccess import (
    get_abstract,
    get_acknowledgements,
    get_contributors,
    get_affiliations,
    get_date,
    get_reference_list,
    get_sections
)

class Chapter:
    """Auxiliary class to parse a chapter from a book."""
    @property
    def abstract(self) -> Optional[str]:
        """Abstract of the chapter."""
        return get_abstract(self._chapter_meta)

    @property
    def acknowledgements(self) -> Optional[str]:
        """Acknowledgements of the chapter."""
        return get_acknowledgements(self._chapter_back)

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
    def full_text(self) -> Optional[str]:
        """Raw full text of the chapter in JATS format."""
        if self._chapter_body is not None:
            return etree.tostring(self._chapter_body, encoding="unicode")

    @property
    def isbn_electronic(self) -> Optional[str]:
        """ISBN of the electronic version of the book."""
        return get_attr(self._book_meta, 'isbn', 'content-type', 'epub')

    @property
    def isbn_print(self) -> Optional[str]:
        """ISBN of the print version of the book."""
        return get_attr(self._book_meta, 'isbn', 'content-type', 'ppub')

    @property
    def parsed_text(self) -> list[Section]:
        """Parsed chapter's text divided into sections.
        
        Returns:
            list[Section]: A list of Section objects containing the
            `section_id`, `section_title`, and `text`.
        """
        return get_sections(self._chapter_body)

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
    def references(self) -> list[Reference]:
        """References of the chapter.
        
        Returns:
            list[Reference]: A list of Reference objects containing the
            `ref_list_id`, `ref_list_title`, `ref_id`, `ref_label`, `ref_publication_type`,
            `authors`, `editors`, `names`, `ref_title`, `ref_source`, `ref_year`, `ref_doi`.
        """
        return get_reference_list(self._chapter_back)

    @property
    def title(self) -> Optional[str]:
        """Title of the chapter."""
        return get_text(self._chapter_meta, './/title-group/title')

    def __init__(self, data):
        self._data = data
        self._book_meta = data.find('.//book-meta')
        self._chapter_body = data.find('./book-part/body')
        self._chapter_back = data.find('.//back')
        self._chapter_meta = data.find('.//book-part[@book-part-type="chapter"]/book-part-meta')


    def __repr__(self) -> str:
        return f'Chapter {self.doi}'
