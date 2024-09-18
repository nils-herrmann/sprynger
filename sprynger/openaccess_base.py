"""Module with the OpenAccess base class."""
from typing import Literal, Optional, Union

from sprynger.retrieve import Retrieve
from sprynger.utils.fetch import detect_id_type
from sprynger.utils.data_structures import OpenAcessParagraph


class OpenAccessBase(Retrieve):
    """Base class to retrieve OpenAccess from the Springer OpenAccess API."""
    def get_paragraphs(self, document_type: str) -> list[list[OpenAcessParagraph]]:
        """Paragraphs of the OpenAccess document.

        Returns:
            list[OpenAcessParagraph]: A list of OpenAcessParagraph objects containing the 
            `paragraph_id`, `section_id`, `section_title`, and `text`.
        """
        # Extract the paragraphs from the XML
        documents = []
        for document in self.xml.findall(f'.//{document_type}'):

            paragraphs = []
            sections = document.findall('.//body//sec')
            if len(sections) == 0:
                sections = []
  
            for section in sections:
                section_id = section.get('id')
                section_title = section.find('title').text if section.find('title') is not None else None

                for paragraph in section.findall('p'):
                    paragraph_id = paragraph.get('id')
                    paragraph_text = ''.join(paragraph.itertext())

                    data = OpenAcessParagraph(
                            paragraph_id=paragraph_id,
                            section_id=section_id,
                            section_title=section_title,
                            text=paragraph_text.strip()
                    )
                    paragraphs.append(data)
            documents.append(paragraphs)

        return documents


    def __init__(self,
                identifier: str,
                id_type: Optional[Literal['doi', 'issn', 'isbn']] = None,
                start: int = 1,
                max_results: int = 10,
                cache: bool = True,
                refresh: Union[bool, int] = False):
        """Base class to retrieve OpenAccess from the Springer OpenAccess API."""
        self._id = identifier
        self._id_type = id_type
        self._start = start
        self._max_results = max_results

        # Detect the identifier type if not provided
        if self._id_type is None:
            self._id_type = detect_id_type(self._id)

        super().__init__(identifier=self._id,
                        id_type=self._id_type,
                        api='OpenAccess',
                        start=self._start,
                        max_results=self._max_results,
                        cache=cache,
                        refresh=refresh)
