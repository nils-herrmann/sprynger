"""Module with all the data structures used in the package."""
from collections import namedtuple

def create_namedtuple(name: str, fields: list, defaults=None):
    """Create a namedtuple with default values."""
    default_list = [defaults] * len(fields)
    return namedtuple(name, fields, defaults=default_list)

#############################
#          Metadata         #
#############################
fields_metadata_results = ['total', 'start', 'pageLength', 'recordsRetrieved']
MetadataResult = create_namedtuple('MetadataResult', fields_metadata_results)

fields_metadata_record = ['contentType', 'identifier', 'language', 'url',
                          'url_format', 'url_platform' ,'title', 'creators',
                          'publicationName', 'openaccess', 
                          'doi', 'publisher', 'publicationDate',
                          'publicationType', 'issn', 'volume', 'number', 'genre', 
                          'startingPage', 'endingPage', 'journalId',
                          'copyright', 'abstract', 'subjects']
MetadataRecord = create_namedtuple('MetadataRecord', fields_metadata_record)

fields_metadata_creator = ['creator', 'ORCID']
MetadataCreator = create_namedtuple('MetadataCreator', fields_metadata_creator)

fields_metadata_facets = ['facet', 'value', 'count']
MetadataFacets = create_namedtuple('MetadataFacets', fields_metadata_facets)

#############################
#         Open Access       #
#############################

# Open Access Paragraph
fields_openaccess_paragraphs = ['paragraph_id', 'section_id', 'section_title', 'text']
Paragraph = create_namedtuple('Paragraph', fields_openaccess_paragraphs)
