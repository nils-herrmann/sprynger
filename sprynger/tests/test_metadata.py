"""Tests for the metadata module."""
import pytest

from sprynger import init
from sprynger import Metadata, DocumentMetadata
from sprynger.utils.data_structures import MetadataCreator, MetadataFacets, MetadataRecord, MetadataResult

init()

journal_metadata = Metadata('3004-9261', start=1, nr_results=2, refresh=True)
book_metadata = Metadata('978-1-0716-1418-1', start=1, nr_results=3, refresh=30)
single_article_metadata = DocumentMetadata('10.1007/s10660-023-09761-x', refresh=30)
meta_pagination = Metadata('2662-9984', nr_results=30, refresh=30)
with pytest.warns(UserWarning):
    article_metadata = Metadata('10.1186/s43593-023-00053-3', refresh=30)


def test_book():
    """Test the book metadata."""
    for book in book_metadata.records:
        assert book.contentType == 'Chapter'
        assert book.publicationName == 'An Introduction to Statistical Learning'


def test_single_article():
    """Test the single article metadata."""
    expected_metadata = MetadataRecord(
        contentType="Article",
        identifier="doi:10.1007/s10660-023-09761-x",
        language="en",
        url="http://dx.doi.org/10.1007/s10660-023-09761-x",
        url_format="",
        url_platform="",
        title="From clicks to consequences: a multi-method review of online grocery shopping",
        creators=[
            MetadataCreator(creator="Shroff, Arvind", ORCID="0000-0002-8544-5361"),
            MetadataCreator(creator="Kumar, Satish", ORCID="0000-0001-5200-1476"),
            MetadataCreator(creator="Martinez, Luisa M.", ORCID=None),
            MetadataCreator(creator="Pandey, Nitesh", ORCID=None),
        ],
        publicationName="Electronic Commerce Research",
        openaccess=False,
        doi="10.1007/s10660-023-09761-x",
        publisher="Springer",
        publicationDate="2024-06-01",
        publicationType="Journal",
        issn="1572-9362",
        volume=24,
        number=2,
        genre="OriginalPaper",
        startingPage=925,
        endingPage=964,
        journalId=10660,
        copyright="©2023 The Author(s), under exclusive licence to Springer Science+Business Media, LLC, part of Springer Nature",
        abstract="The academic interest in Online Grocery Shopping (OGS) has proliferated in retailing and business management over the past two decades. Previous research on OGS was primarily focused on consumer-level consequences such as purchase intention, purchase decision, and post-purchase behavior. However, there is a lack of literature integrating intrinsic and extrinsic factors that influence the growth of OGS and its impact on purchase outcomes. To address this, we conduct a multi-method review combining traits of a systematic literature review and bibliometric analysis. Analyzing 145 articles through word cloud and keyword co-occurrence analysis, we identify publication trends (top journals, articles) and nine thematic clusters. We develop an integrated conceptual framework encompassing the antecedents, mediators, moderators, and consequences of OGS. Finally, we outline future research directions using Theory-Context-Characteristics-Methods framework to serve as a reference point for future researchers working in OGS.",
        subjects=[
            "Business and Management",
            "IT in Business",
            "Data Structures and Information Theory",
            "Operations Research/Decision Theory",
            "Computer Communication Networks",
            "Business and Management, general",
            "e-Commerce/e-business",
        ],
    )
    assert single_article_metadata.metadata == expected_metadata


def test_journal():
    """Test the journal metadata."""
    for article in journal_metadata.records:
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

    expected = MetadataFacets(facet='subject', value='Physics', count='1')
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


def test_wrong_id_type():
    """Test the wrong identifier type."""
    try:
        Metadata('12345678901234567890')
    except ValueError as e:
        assert str(e) == 'Invalid identifier'
    else:
        raise AssertionError('ValueError not raised')


def test_warning():
    """Test the warning message and get the article metadata."""
    w_message = r'Too many results requested\. 1 document\(s\) found but 10 requested\.'
    with pytest.warns(UserWarning, match=w_message):
        Metadata('10.1186/s43593-023-00053-3', refresh=30)
