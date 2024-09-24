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
OpenAcessParagraph = create_namedtuple('OpenAcessParagraph', fields_openaccess_paragraphs)

# Open Access Journal/Article
fields_openaccess_article_meta = ['article_type', 'language', 'publisher_id', 'manuscript', 'doi']
ArticleMeta = create_namedtuple('ArticleMeta', fields_openaccess_article_meta)

fields_openaccess_journal_meta = ['publisher_id', 'doi', 'journal_title',
                                  'journal_abbrev_title', 'issn_print', 'issn_electronic',
                                  'publisher_name', 'publisher_loc']
JournalMeta = create_namedtuple('JournalMeta', fields_openaccess_journal_meta)

# Open Access Book/Chapter
fields_openaccess_book_meta = ['doi', 'publisher_id', 'book_title_id', 'pub_date',
                               'isbn_print', 'isbn_electronic', 'publisher_name',
                               'publisher_loc']
BookMeta = create_namedtuple('BookMeta', fields_openaccess_book_meta)

fields_openaccess_chaper_meta = ['doi', 'chapter']
ChapterMeta = create_namedtuple('ChapterMeta', fields_openaccess_chaper_meta)
