"""Module with auxiliary functions to parse OpenAccess documents."""
from sprynger.utils.data_structures import OpenAcessParagraph

def get_paragraphs(xml_data) -> list[OpenAcessParagraph]:
    """Paragraphs of the OpenAccess document.

    Returns:
        list[OpenAcessParagraph]: A list of OpenAcessParagraph objects containing the 
        `paragraph_id`, `section_id`, `section_title`, and `text`.
    """
    # Extract the paragraphs from the XML
    section_paragraphs = []
    sections = xml_data.findall('.//body//sec')
    if len(sections) == 0:
        sections = []

    for section in sections:
        section_id = section.get('id')
        section_title = section.find('title').text if section.find('title') is not None else None

        for paragraph in section.findall('p'):
            paragraph_id = paragraph.get('id')
            paragraph_text = ''.join(paragraph.itertext())

            paragraph_data = OpenAcessParagraph(
                paragraph_id=paragraph_id,
                section_id=section_id,
                section_title=section_title,
                text=paragraph_text.strip()
            )
            section_paragraphs.append(paragraph_data)

    return section_paragraphs
