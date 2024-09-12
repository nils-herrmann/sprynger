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