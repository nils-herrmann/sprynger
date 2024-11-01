"""Module with auxiliary functions to parse OpenAccess documents."""
from typing import Optional

from lxml.etree import _Element

from sprynger.utils.data_structures import Affiliation, Contributor, Date, Paragraph, Reference
from sprynger.utils.parse import get_attr, get_text, make_int_if_possible, stringify_descendants


def affs_to_dict(affs) -> dict[str, Affiliation]:
    """Auxiliary function to query the affiliations by their number."""
    return {aff.nr: aff for aff in affs}


def get_acknowledgements(back: _Element) -> Optional[str]:
    """Parse the acknowledgements of the document."""
    paragraphs = []
    if back is not None:
        for p in back.findall('.//ack/p', []):
            paragraphs.append(get_text(p, '.'))
    return '\n'.join(paragraphs) or None


def get_affiliations(data: _Element) -> list[Affiliation]:
    """Parse the affiliations of the document."""
    affiliations = []
    if data is not None:
        for contrib_group in data.findall('.//contrib-group'):
            contribution_group = contrib_group.get('content-type')
            for a in contrib_group.findall('.//aff'):
                institution = a.find('.//institution-wrap')
                new_aff = Affiliation(
                    type=contribution_group,
                    ref_nr=a.get('id'),
                    ror=get_attr(institution, 'institution-id', 'institution-id-type', 'ROR'),
                    grid=get_attr(institution, 'institution-id', 'institution-id-type', 'GRID'),
                    isni=get_attr(institution, 'institution-id', 'institution-id-type', 'ISNI'),
                    division=get_attr(institution, 'institution', 'content-type', 'org-division'),
                    name=get_attr(institution, 'institution', 'content-type', 'org-name'),
                    city=get_attr(a, 'addr-line', 'content-type', 'city'),
                    country=get_text(a, './/country')
                )
                affiliations.append(new_aff)
    return affiliations


def get_contributors(data: _Element) -> list[Contributor]:
    """Parse the contributors of the document and matcg them with their affiliations."""
    contributors = []
    if data is not None:
        for c in data.findall('.//contrib'):
            # Get affiliation
            affs_nr = []
            for aff_ref in c.findall('.//xref[@ref-type="aff"]'):
                aff_nr = aff_ref.get('rid')
                affs_nr.append(aff_nr)

            # Get contributor data
            new_contrib = Contributor(
                type=c.get('contrib-type'),
                nr=c.get('id'),
                orcid=get_attr(c, 'contrib-id', 'contrib-id-type', 'orcid'),
                surname=get_text(c, './/name/surname'),
                given_name=get_text(c, './/name/given-names'),
                email=get_text(c, './/email'),
                affiliations_ref_nr=affs_nr
            )
            contributors.append(new_contrib)
    return contributors


def get_date(date_node: _Element) -> Date:
    """Auxiliary function to extract date information from a date node."""
    return Date(day=make_int_if_possible(get_text(date_node, './/day')),
                month=make_int_if_possible(get_text(date_node, './/month')),
                year=make_int_if_possible(get_text(date_node, './/year')))


def get_paragraphs(xml) -> list[Paragraph]:
    """Paragraphs of the OpenAccess document.

    Returns:
        list[Paragraph]: A list of Paragraph objects containing the 
        `paragraph_id`, `section_id`, `section_title`, and `text`.
    """
    if xml is not None:
        parsed_paragraphs = []
        for paragraph in xml.findall('.//p[@id]'):
            paragraph_id = paragraph.get('id')
            paragraph_text = ''.join(paragraph.itertext())

            parent = paragraph.getparent()
            section_id = parent.get('id')
            section_title = get_text(parent, 'title')


            paragraph_data = Paragraph(
                paragraph_id=paragraph_id,
                section_id=section_id,
                section_title=section_title,
                text=paragraph_text.strip()
            )
            parsed_paragraphs.append(paragraph_data)

        return parsed_paragraphs
    return []

def _get_doi(ref_node: _Element) -> Optional[str]:
    """Parse DOIs from a reference node."""
    doi = get_attr(ref_node, "pub-id", "pub-id-type", "doi")
    if doi is None:
        doi = get_attr(ref_node, "ext-link", "ext-link-type", "doi")
        if doi is not None:
            doi = doi.replace("https://doi.org/", "")
    return doi

def _get_names(ref_node: _Element) -> Optional[list[str]]:
    """Parse names from a reference node."""
    names = []
    for person in ref_node.findall('name'):
        given_name = stringify_descendants(person.find('given-names'))
        surname = stringify_descendants(person.find('surname'))
        name = f'{given_name} {surname}'
        names.append(name)
    return names

def _get_names_from_group(ref_node: _Element, person_group_type: str) -> Optional[list[str]]:
    """Parse names from a person-group node."""
    names = []
    group_node = ref_node.find(f'./person-group[@person-group-type="{person_group_type}"]')
    if group_node is not None:
        names = _get_names(group_node)
    return names

def _get_reference(reference: _Element) -> Optional[_Element]:
    """Get reference from one of the three possible positions."""
    for tag in ["mixed-citation", "element-citation", "citation"]:
        ref = reference.find(tag)
        if ref is not None:
            return ref
    return None

def get_reference_list(back: _Element) -> list[Reference]:
    """Parse the references of the document."""
    new_ref_list = []
    if back is not None:
        for ref_list in back.findall('.//ref-list[@id]'):

            ref_list_id = ref_list.get('id')
            ref_list_title = get_text(ref_list, './/title')
            for ref in ref_list.findall('.//ref[@id]'):
                ref_id = ref.get('id')
                ref_label = get_text(ref, 'label')
                ref = _get_reference(ref)
                # Avoid unbound variables
                ref_publication_type, authors, editors, names = None, [], [], []
                ref_title, ref_source, ref_year, ref_doi = None, None, None, None
                if ref is not None:
                    ref_publication_type = ref.get('publication-type') or ref.get('citation-type')
                    if ref_publication_type is not None:
                        # Get the title from the article-title tag or the whole reference
                        ref_title = get_text(ref, "article-title")
                        if ref_title is None:
                            ref_title = stringify_descendants(ref)
                        # Get the authors from the name tag or the person-group tag
                        if ref.find('name') is not None:
                            names = _get_names(ref)
                        else:
                            authors = _get_names_from_group(ref, "author")
                            editors = _get_names_from_group(ref, "editor")
                        # Get the source, year and DOI
                        ref_source = get_text(ref, "source")
                        ref_year = get_text(ref, "year")
                        # Get the DOI
                        ref_doi = _get_doi(ref)

                reference = Reference(
                    ref_list_id=ref_list_id,
                    ref_list_title=ref_list_title,
                    ref_id=ref_id,
                    ref_label=ref_label,
                    ref_publication_type=ref_publication_type,
                    authors=authors,
                    editors=editors,
                    names=names,
                    ref_title=ref_title,
                    ref_source=ref_source,
                    ref_year=ref_year,
                    ref_doi=ref_doi
                )

                new_ref_list.append(reference)
    return new_ref_list
