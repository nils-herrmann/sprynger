from collections import namedtuple

fields_metadata_record = ['contentType', 'identifier', 'language', 'url', 'url_format', 'url_platform' ,'title', 'creators', 'publicationName', 'openaccess', 
                          'doi', 'publisher', 'publicationDate', 'publicationType', 'issn', 'volume', 'number', 'genre', 
                          'startingPage', 'endingPage', 'journalId', 'copyright', 'abstract', 'subjects']
MetadataRecord = namedtuple('MetadataRecord',
                            fields_metadata_record,
                            defaults=[None] * len(fields_metadata_record))

fields_metadata_creator = ['creator', 'ORCID']
MetadataCreator = namedtuple('MetadataCreator',
                            fields_metadata_creator,
                            defaults=[None] * len(fields_metadata_creator))

fields_metadata_facets = ['facet', 'value', 'count']
MetadataFacets = namedtuple('MetadataFacets',
                            fields_metadata_facets,
                            defaults=[None] * len(fields_metadata_facets))

fields_openaccess_paragraphs = ['paragraph_id', 'section_id', 'section_title', 'text']
OpenAcessParagraph = namedtuple('OpenAcessParagraph',
                                fields_openaccess_paragraphs,
                                defaults=[None] * len(fields_openaccess_paragraphs))

fields_openaccess_article_meta = ['publisher_id', 'manuscript', 'doi']
ArticleMeta = namedtuple('ArticleMeta',
                         fields_openaccess_article_meta,
                         defaults=[None] * len(fields_openaccess_article_meta))

fields_openaccess_book_meta = ['doi', 'chapter']
ChapterMeta = namedtuple('ChapterMeta',
                      fields_openaccess_book_meta,
                      defaults=[None] * len(fields_openaccess_book_meta))

fields_openaccess_journal_meta = ['publisher_id', 'doi', 'journal_title',
                                  'journal_abbrev_title', 'issn_print', 'issn_electronic',
                                  'publisher_name', 'publisher_loc']
JournalMeta = namedtuple('JournalMeta',
                         fields_openaccess_journal_meta,
                         defaults=[None] * len(fields_openaccess_journal_meta))

fields_openaccess_book_meta = ['doi', 'publisher_id', 'book_title_id', 'pub_date',
                               'isbn_print', 'isbn_electronic', 'publisher_name',
                               'publisher_loc']
BookMeta = namedtuple('BookMeta',
                      fields_openaccess_book_meta,
                      defaults=[None] * len(fields_openaccess_book_meta))
