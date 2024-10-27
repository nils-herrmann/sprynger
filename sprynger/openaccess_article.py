"""Module with the Article class for the OpenAccess class."""
from typing import Optional

from sprynger.utils.data_structures import Affiliation, Contributor, Date, Paragraph
from sprynger.utils.parse import get_attr, get_text
from sprynger.utils.parse_openaccess import (
    affs_to_dict,
    get_contributors,
    get_affiliations,
    get_date,
    get_paragraphs,
)

class Article:
    """Auxiliary class to parse an article from a journal."""
    @property
    def affiliations(self) -> list[Affiliation]:
        """List of affiliations of the collaborators of the article. Each affiliation is represented
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
    def article_type(self) -> Optional[str]:
        """Type of the article."""
        return self._data.get('article-type')

    @property
    def contributors(self) -> list[Contributor]:
        """List of contributors of the article. Each contributor is represented as a named tuple
        with the following fields:
        `type`, `nr`, `orcid`, `surname`, `given_name`, `email`, `affiliations_ref_nr`.

        Note: To match contributors with affiliations use the contributor's `affiliations_ref_nr`
        and the affiliation's `ref_nr`.
        """
        return get_contributors(self._article_meta)

    @property
    def date_epub(self) -> Date:
        """Electronic publication date of the article."""
        date_node = self._article_meta.find('.//pub-date[@publication-format="electronic"]')
        return get_date(date_node)

    @property
    def date_ppub(self) -> Date:
        """Print publication date of the article."""
        date_node = self._article_meta.find('.//pub-date[@publication-format="print"]')
        return get_date(date_node)

    @property
    def date_registration(self) -> Date:
        """Registration date of the article."""
        date_node = self._article_meta.find('.//history/date[@date-type="registration"]')
        return get_date(date_node)

    @property
    def date_received(self) -> Date:
        """Date when article was recieved."""
        date_node = self._article_meta.find('.//history/date[@date-type="received"]')
        return get_date(date_node)

    @property
    def date_accepted(self) -> Date:
        """Accepted date of the article."""
        date_node = self._article_meta.find('.//history/date[@date-type="accepted"]')
        return get_date(date_node)

    @property
    def date_online(self) -> Date:
        """Online date of the article."""
        date_node = self._article_meta.find('.//history/date[@date-type="online"]')
        return get_date(date_node)

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
