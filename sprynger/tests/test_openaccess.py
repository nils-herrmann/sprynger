"""Tests for the OpenAccess class."""
from sprynger import init, OpenAccess
from sprynger.openaccess import Article, Chapter
from sprynger.utils.data_structures import Affiliation, Contributor, Date, Paragraph

init()

book = OpenAccess(isbn="978-3-031-63500-7", start=1, nr_results=2, refresh=30)
chapter = OpenAccess("doi:10.1007/978-3-031-61874-1_5", refresh=30)
chapter_with_text = OpenAccess(doi="10.1007/978-3-031-24498-8_7", refresh=30)
book_pagination = OpenAccess(isbn='978-3-031-63498-7', nr_results=30, refresh=30)

journal = OpenAccess(issn="2198-6053", start=4, nr_results=3, refresh=30)
journal_pagination = OpenAccess('issn:2198-6584', nr_results=26, refresh=True)
article = OpenAccess(doi="10.1007/s40747-024-01577-y", refresh=30)


def test_article_affiliations():
    """Test the affiliations of the article."""
    expected = [
        Affiliation(type=None, ref_nr='Aff1', ror='https://ror.org/04z7qrj66', grid='grid.412518.b', isni='0000 0001 0008 0619', division='College of Information Engineering', name='Shanghai Maritime University', city='Shanghai', country='China'),
        Affiliation(type=None, ref_nr='Aff2', ror='https://ror.org/05k2j8e48', grid='grid.495244.a', isni='0000 0004 1761 5722', division='College of Artificial Intelligence', name='Jiangxi University of Technology', city='Jiangxi', country='China'),
        Affiliation(type=None, ref_nr='Aff3', ror='https://ror.org/04z7qrj66', grid='grid.412518.b', isni='0000 0001 0008 0619', division='College of Merchant Marine', name='Shanghai Maritime University', city='Shanghai', country='China')
        ]
    for a in article:
        assert a.affiliations == expected


def test_article_contributors():
    """Test the contributors of the article."""
    expected = [
        Contributor(type='author', nr='Au1', orcid='http://orcid.org/0000-0002-1606-3511', surname='Hu', given_name='Zhanhui', email=None, affiliations_ref_nr=['Aff1']),
        Contributor(type='author', nr='Au2', orcid=None, surname='Liu', given_name='Guangzhong', email='gzhliu@shmtu.edu.cn', affiliations_ref_nr=['Aff1']),
        Contributor(type='author', nr='Au3', orcid=None, surname='Li', given_name='Yanping', email=None, affiliations_ref_nr=['Aff2']),
        Contributor(type='author', nr='Au4', orcid=None, surname='Zhuang', given_name='Siqing', email=None, affiliations_ref_nr=['Aff3'])
        ]
    for a in article:
        assert a.contributors == expected


def test_article_dates():
    """Test the dates of the article."""
    expected_date_accepted = Date(year=2024, month=7, day=21)
    expected_date_epub = Date(year=2024, month=9, day=9)
    expected_date_online = Date(year=2024, month=9, day=9)
    expected_date_ppub = Date(year=2024, month=12, day=None)
    expected_date_received = Date(year=2024, month=4, day=12)
    expected_date_registration = Date(year=2024, month=7, day=24)

    for a in article:
        assert a.date_accepted == expected_date_accepted
        assert a.date_epub == expected_date_epub
        assert a.date_online == expected_date_online
        assert a.date_ppub == expected_date_ppub
        assert a.date_received == expected_date_received
        assert a.date_registration == expected_date_registration


def test_article_meta():
    """Test the article meta-data."""
    for a in article:
        assert a.article_type == 'research-article'
        assert a.language == 'en'
        assert a.publisher_id == 's40747-024-01577-y'
        assert a.manuscript == '1577'
        assert a.doi == '10.1007/s40747-024-01577-y'
        assert a.title == 'SAGB: self-attention with gate and BiGRU network for intrusion detection'


def test_book_meta():
    """Test the book meta data."""
    for chapter in book:
        assert chapter.book_doi == "10.1007/978-3-031-63501-4"
        assert chapter.publisher_id == "978-3-031-63501-4"
        assert chapter.book_title == "Automated Reasoning"
        assert chapter.book_title_id == "631234"
        assert chapter.book_sub_title == "12th International Joint Conference, IJCAR 2024, Nancy, France, July 3–6, 2024, Proceedings, Part II"
        assert chapter.book_pub_date == "2024-01-01"
        assert chapter.isbn_print == "978-3-031-63500-7"
        assert chapter.isbn_electronic == "978-3-031-63501-4"
        assert chapter.publisher_name == "Springer Nature Switzerland"
        assert chapter.publisher_loc == "Cham"


def test_chapter_affiliations():
    """Test the affiliations of the chapter."""
    expected_affiliations = [
        Affiliation(type='book author', ref_nr='Aff1', ror='https://ror.org/00d7xrm67', grid='grid.410413.3', isni='0000 0001 2294 748X', division='Institute of Software Technology', name='Graz University of Technology', city='Graz', country='Austria'),
        Affiliation(type='book author', ref_nr='Aff2', ror=None, grid='grid.426094.d', isni='0000 0004 0625 6437', division='Corporate Technology', name='Siemens (Austria)', city='Wien', country='Austria'),
        Affiliation(type='book author', ref_nr='Aff3', ror='https://ror.org/03yxnpp24', grid='grid.9224.d', isni='0000 0001 2168 1229', division='ETS de Ingeniería Informática', name='University of Seville', city='Sevilla', country='Spain'),
        Affiliation(type=None, ref_nr='Aff4', ror='https://ror.org/00d7xrm67', grid='grid.410413.3', isni='0000 0001 2294 748X', division='Institute of Software Technology', name='Graz University of Technology', city='Graz', country='Austria'),
        Affiliation(type=None, ref_nr='Aff5', ror=None, grid='grid.426094.d', isni='0000 0004 0625 6437', division='Corporate Technology', name='Siemens (Austria)', city='Wien', country='Austria'),
        Affiliation(type=None, ref_nr='Aff6', ror='https://ror.org/03yxnpp24', grid='grid.9224.d', isni='0000 0001 2168 1229', division='ETS de Ingeniería Informática', name='University of Seville', city='Sevilla', country='Spain')
        ]
    for one_chapter in chapter:
        assert one_chapter.affiliations == expected_affiliations


def test_chapter_contributors():
    """Test the contributors of the chapter."""
    expected_contributors = [
        Contributor(type='author', nr=None, orcid=None, surname='Felfernig', given_name='Alexander', email='alexander.felfernig@ist.tugraz.at', affiliations_ref_nr=['Aff1']),
        Contributor(type='author', nr=None, orcid=None, surname='Falkner', given_name='Andreas', email='andreas.a.falkner@siemens.com', affiliations_ref_nr=['Aff2']),
        Contributor(type='author', nr=None, orcid=None, surname='Benavides', given_name='David', email='benavides@us.es', affiliations_ref_nr=['Aff3']),
        Contributor(type='author', nr=None, orcid=None, surname='Felfernig', given_name='Alexander', email=None, affiliations_ref_nr=['Aff4']),
        Contributor(type='author', nr=None, orcid=None, surname='Falkner', given_name='Andreas', email=None, affiliations_ref_nr=['Aff5']),
        Contributor(type='author', nr=None, orcid=None, surname='Benavides', given_name='David', email=None, affiliations_ref_nr=['Aff6'])
        ]
    for one_chapter in chapter:
        assert one_chapter.contributors == expected_contributors


def test_chapter_dates():
    """Test the dates of the chapter."""
    expected_date_epub = Date(year=2024, month=6, day=30)
    expected_date_online = Date(year=2024, month=6, day=30)
    expected_date_ppub = Date(year=None, month=None, day=None)
    expected_date_registration = Date(year=2024, month=5, day=27)

    for one_chapter in chapter:
        assert one_chapter.date_epub == expected_date_epub
        assert one_chapter.date_online == expected_date_online
        assert one_chapter.date_ppub == expected_date_ppub
        assert one_chapter.date_registration == expected_date_registration


def test_chapter_meta():
    """Test the chapter meta data."""
    for one_chapter in chapter:
        assert one_chapter.doi == '10.1007/978-3-031-61874-1_5'
        assert one_chapter.chapter_nr == 5
        assert one_chapter.title == 'Tools and Applications'

    assert isinstance(book[0], Chapter)


def test_iterable():
    """Test the lengths"""
    assert len(book) == 2
    for book_chapter in book:
        assert isinstance(book_chapter, Chapter)

    assert len(journal) == 3
    for journal_article in journal:
        assert isinstance(journal_article, Article)


def test_journal_meta():
    """Test the journal meta-data."""
    for article in journal:
        assert article.journal_publisher_id == '40747'
        assert article.journal_doi is None
        assert article.journal_title == 'Complex & Intelligent Systems'
        assert article.journal_abbrev_title == 'Complex Intell. Syst.'
        assert article.issn_print == '2199-4536'
        assert article.issn_electronic == '2198-6053'
        assert article.publisher_name == 'Springer International Publishing'
        assert article.publisher_loc == 'Cham'


def test_paragraphs():
    """Test the paragraphs."""
    assert len(chapter[0].paragraphs) == 1
    expected_paragraph = Paragraph(paragraph_id='Par1',
                                            section_id='Abs1',
                                            section_title='Abstract',
                                            text='Feature Models (FMs) are not only an active scientific topic but they are supported by many tools from industry and academia. In this chapter, we provide an overview of example feature modelling tools and corresponding FM configurator applications. In our discussion, we first focus on different tools supporting the design of FMs. Thereafter, we provide an overview of tools that also support FM analysis. Finally, we discuss different existing FM configurator applications.')
    assert chapter[0].paragraphs[0] == expected_paragraph

    assert len(chapter_with_text[0].paragraphs) == 49
    expected_paragraph = Paragraph(paragraph_id='Par5',
                                            section_id='Sec1',
                                            section_title='Introduction',
                                            text='In this work, I aim to provide a better understanding of the governanceGovernance/human factors that Data Scientist and organizations should be aware of. To address this challengeChallenges, I will answer fundamental research questions for the domain.')
    assert chapter_with_text[0].paragraphs[4] == expected_paragraph

    assert len(article[0].paragraphs) == 70
    expected_paragraph = Paragraph(paragraph_id='Par5',
                                            section_id='Sec1',
                                            section_title='Introduction',
                                            text="With the diversification and complexity of intrusion methods and the maturity of machine learning algorithms, studying intrusion detection based on machine learning is a hot topic for scientists. The methods based on machine learning include those based on behavior and statistics, whose main idea is to extract the features of the network's traffic and then use traffic features for modeling and training to obtain a classification model that can identify and classify the new traffic in real-time, which has relatively low complexity and good performance, but still has some shortcomings, mainly reflected in:The normal traffic data is more than abnormal traffic for the training sample, and the data imbalance problem will lead to low precision.Most studies emphasize the model's precision in the data set while neglecting to pay attention to the detection rate of the minority attack categories. However, the attacks of the minority categories often cause more damage to the network than the majority categories' attacks.Deep learning [4] is an effective method to solve the shortcomings of shallow machine learning networks. The CNN and RNN have been widely used in classification problems [5] and regression problems [6]. Some methods based on RNN can learn temporal sequence features, but serial-based sequence training has low convergence efficiency and low accuracy.Some machine learning, such as Random Forest (RF) and Decision tree (DT), only learn shallow features, whose effect of multiple classification precision is not good. Deep learning, such as CNN and RNN, made some achievements, but for some large datasets, the generalization ability is poor and can not be calculated in parallel.")
    assert article[0].paragraphs[4] == expected_paragraph


def test_pagination():
    """Test the pagination."""
    assert len(book_pagination) == 27
    dois = set([chapter.doi for chapter in book_pagination])
    assert len(dois) == 27

    assert len(journal_pagination) == 26
    dois = set([article.doi for article in journal_pagination])
    assert len(dois) == 26
