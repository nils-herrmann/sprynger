"""Tests for the Meta class."""
from sprynger import init
from sprynger import Metadata
from sprynger.utils.data_structures import (MetadataCreator,
                                            MetadataFacets,
                                            MetadataRecord,
                                            MetadataResult)

init()

journal_metadata = Metadata(issn='3004-9261', start=1, nr_results=2, refresh=30)
book_metadata = Metadata(isbn='978-1-0716-1418-1', start=1, nr_results=3, refresh=30)
meta_pagination = Metadata('issn:2662-9984', nr_results=30, refresh=True)
article_metadata = Metadata('doi:10.1186/s43593-023-00053-3', refresh=30)


def test_book():
    """Test the book metadata."""
    for book in book_metadata.records:
        assert book.contentType == 'Chapter'
        assert book.publicationName == 'An Introduction to Statistical Learning'


def test_journal():
    """Test the journal metadata."""
    for article in journal_metadata:
        assert article.publicationName == 'Discover Applied Sciences'
        assert article.issn == '3004-9261'
        assert article.journalId == 42452


def test_len():
    """Test the length of the metadata."""
    assert len(article_metadata.records) == 1

    assert len(journal_metadata.records) == 2
    assert len(journal_metadata) == 2

    assert len(book_metadata.records) == 3
    assert len(book_metadata) == 3


def test_factets():
    """Test the facets."""
    assert len(article_metadata.facets) == 11

    expected = MetadataFacets(facet='subject', value='Physics', count=1)
    assert article_metadata.facets[1] == expected


def test_records():
    """Test the records."""
    expected = MetadataRecord(contentType='Article',
                              identifier='doi:10.1186/s43593-023-00053-3',
                              language='en',
                              url='http://dx.doi.org/10.1186/s43593-023-00053-3',
                              url_format='',
                              url_platform='',
                              title='Highly efficient flexible structured metasurface by roll-to-roll printing for diurnal radiative cooling',
                              creators=[MetadataCreator(creator='Lin, Keng-Te', ORCID=None),
                                        MetadataCreator(creator='Nian, Xianbo', ORCID=None),
                                        MetadataCreator(creator='Li, Ke', ORCID=None),
                                        MetadataCreator(creator='Han, Jihong', ORCID=None),
                                        MetadataCreator(creator='Zheng, Nan', ORCID=None),
                                        MetadataCreator(creator='Lu, Xiaokang', ORCID=None),
                                        MetadataCreator(creator='Guo, Chunsheng', ORCID=None),
                                        MetadataCreator(creator='Lin, Han', ORCID=None),
                                        MetadataCreator(creator='Jia, Baohua', ORCID='0000-0002-6703-477X')],
                              publicationName='eLight',
                              openaccess=True,
                              doi='10.1186/s43593-023-00053-3',
                              publisher='Springer',
                              publicationDate='2023-10-25',
                              publicationType='Journal',
                              issn='2662-8643',
                              volume=3,
                              number=1,
                              genre=['OriginalPaper', 'Research Article'],
                              startingPage=1,endingPage=12, journalId=43593,
                              copyright='©2023 The Author(s)',
                              abstract='An ideal radiative cooler requires accurate spectral control capability to achieve efficient thermal emission in the atmospheric transparency window (8–13\xa0μm), low solar absorption, good stability, scalability, and a simple structure for effective diurnal radiative cooling. Flexible cooling films made from polymer relying on polymer intrinsic absorbance represent a cost-effective solution but lack accuracy in spectral control. Here, we propose and demonstrate a metasurface concept enabled by periodically arranged three-dimensional (3D) trench-like structures in a thin layer of polymer for high-performance radiative cooling. The structured polymer metasurface radiative cooler is manufactured by a roll-to-roll printing method. It exhibits superior spectral breadth and selectivity, which offers outstanding omnidirectional absorption/emission (96.1%) in the atmospheric transparency window, low solar absorption (4.8%), and high stability. Impressive cooling power of 129.8 W m −2 and temperature deduction of 7\xa0°C on a clear sky midday have been achieved, promising broad practical applications in energy saving and passive heat dispersion fields.',
                              subjects=['Physics', 'Optics, Lasers, Photonics, Optical Devices'])
    assert article_metadata.records[0] == expected


def test_pagination():
    """Test the pagination."""
    assert len(meta_pagination.records) == 30
    ids = set([record.identifier for record in meta_pagination.records])
    assert len(ids) == 30


def test_results():
    """Test the results."""
    expected = MetadataResult(total=1, start=1, pageLength=10, recordsRetrieved=1)
    assert article_metadata.results == expected
