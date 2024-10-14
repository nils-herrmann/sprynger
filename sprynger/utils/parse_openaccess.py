"""Module with auxiliary functions to parse OpenAccess documents."""
from sprynger.utils.data_structures import Paragraph
from sprynger.utils.parse import get_text

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
