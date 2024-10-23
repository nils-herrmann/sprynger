"""Module with auxiliary functions to parse OpenAccess documents."""
from lxml.etree import _Element

from sprynger.utils.data_structures import Affiliation, Contributor, Date, Paragraph
from sprynger.utils.parse import get_attr, get_text, make_int_if_possible


def affs_to_dict(affs) -> dict[str, Affiliation]:
    """Auxiliary function to query the affiliations by their number."""
    return {aff.nr: aff for aff in affs}


def get_affiliations(data: _Element) -> list[Affiliation]:
    """Parse the affiliations of the document."""
    affiliations = []
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
