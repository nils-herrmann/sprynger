"""Tests for the OpenAccessJournal class."""
from sprynger import init
from sprynger import OpenAccessArticle, OpenAccessJournal
from sprynger.openaccess_journal import _Article
from sprynger.utils.data_structures import ArticleMeta, JournalMeta, OpenAcessParagraph

init()

journal = OpenAccessJournal("2198-6053", start=4, nr_results=3, refresh=30)
journal_pagination = OpenAccessJournal('2198-6584', nr_results=26, refresh=30)
article = OpenAccessArticle("10.1007/s40747-024-01577-y", refresh=30)

def test_article_meta():
    """Test the article meta-data."""
    expected = ArticleMeta(
        article_type = "research-article",
        language="en",
        publisher_id="s40747-024-01577-y",
        manuscript="1577",
        doi="10.1007/s40747-024-01577-y",
    )
    assert article.metadata == expected
    assert isinstance(journal[1].metadata, ArticleMeta)


def test_iterable():
    """Test the lengths of the journal and the articles."""
    assert len(journal) == 3
    for journal_article in journal:
        assert isinstance(journal_article, _Article)


def test_journal_meta():
    """Test the journal meta-data."""
    expected_journal_meta = JournalMeta(
        publisher_id="40747",
        doi=None,
        journal_title="Complex & Intelligent Systems",
        journal_abbrev_title="Complex Intell. Syst.",
        issn_print="2199-4536",
        issn_electronic="2198-6053",
        publisher_name="Springer International Publishing",
        publisher_loc="Cham",
    )
    assert journal.metadata == expected_journal_meta

    expected_article_journal_meta = JournalMeta(publisher_id='40747',
                                        doi=None,
                                        journal_title='Complex & Intelligent Systems',
                                        journal_abbrev_title='Complex Intell. Syst.',
                                        issn_print='2199-4536',
                                        issn_electronic='2198-6053',
                                        publisher_name='Springer International Publishing',
                                        publisher_loc='Cham')

    assert article.journal_metadata == expected_article_journal_meta

def test_pagination():
    """Test the pagination."""
    assert len(journal_pagination) == 26
    dois = set([article.metadata.doi for article in journal_pagination])
    assert len(dois) == 26


def test_paragraphs():
    """Test the paragraphs."""
    assert len(article.paragraphs) == 58

    expected_paragraph = OpenAcessParagraph(
        paragraph_id="Par10",
        section_id="Sec1",
        section_title="Introduction",
        text="It is of great significance to solve these shortcomings, and this paper proposed random undersampling for the majority categories samples and K-Smote oversampling for the minority categories samples to generate a more balanced data set. We also proposed the Self-Attention with Gate mechanism (SAG) to carry out feature extraction between the local and global features and filter irrelevant noise information for enhancing the generalization ability and calculating in parallel. The experimental results show that the precision is much higher than the comparison studies, especially the precision for the minority categories.",
    )
    assert expected_paragraph == article.paragraphs[4]
