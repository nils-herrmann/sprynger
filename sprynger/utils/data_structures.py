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

# Open Access Section
fields_oa_section = ['section_id', 'section_title', 'text']
Section = create_namedtuple('Section', fields_oa_section)

fields_oa_contributor = ['type', 'nr', 'orcid', 'surname', 'given_name', 'email', 'affiliations_ref_nr']
Contributor = create_namedtuple('Contributor', fields_oa_contributor)

fields_oa_aff = ['type', 'ref_nr', 'ror', 'grid', 'isni', 'division', 'name', 'city', 'country']
Affiliation = create_namedtuple('Affiliation', fields_oa_aff)

fields_date = ['year', 'month', 'day']
Date = create_namedtuple('Date', fields_date)

fields_oa_reference = ['ref_list_id', 'ref_list_title', 'ref_id',
                       'ref_label', 'ref_publication_type', 'authors',
                       'editors', 'names',
                       'ref_title', 'ref_source', 'ref_year', 'ref_doi']
Reference = create_namedtuple('Reference', fields_oa_reference)


#############################
#         Meta             #
#############################

fields_meta_url = ['format', 'platform', 'value']
MetaURL = create_namedtuple('MetaURL', fields_meta_url)

fields_meta_discipline = ['id', 'term']
MetaDiscipline = create_namedtuple('MetaDiscipline', fields_meta_discipline)

fields_meta_record = [
    'contentType', 'identifier', 'language',
    'urls', 'title', 'creators',
    'publicationName', 'openaccess', 'doi',
    'publisher', 'publicationDate', 'publicationType',
    'issn', 'eIssn', 'volume',
    'number', 'issueType', 'topicalCollection',
    'genre', 'startingPage', 'endingPage',
    'journalId', 'onlineDate', 'copyright',
    'abstract', 'conferenceInfo', 'keyword',
    'subjects', 'disciplines'
]
MetaRecord = create_namedtuple('MetaRecord', fields_meta_record)
