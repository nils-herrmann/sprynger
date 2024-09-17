"""Tests for the OpenAccessJournal class."""
from sprynger import init
from sprynger import OpenAccessJournal
from sprynger.utils.data_structures import ArticleMeta, JournalMeta, OpenAcessParagraph

init()

journal = OpenAccessJournal("2198-6053", start=4, max_results=3, refresh=30)
article = OpenAccessJournal("10.1007/s40747-024-01577-y", refresh=30)

def test_article_meta():
    """Test the article meta-data."""
    assert len(journal.article_meta) == 3
    expected = ArticleMeta(
        publisher_id="s40747-024-01577-y",
        manuscript="1577",
        doi="10.1007/s40747-024-01577-y",
    )
    assert article.article_meta[0] == expected


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
    assert journal.journal_meta == expected_journal_meta


def test_paragraphs():
    """Test the paragraphs."""
    assert len(journal.paragraphs) == 3

    assert len(article.paragraphs) == 1
    assert len(article.paragraphs[0]) == 58
    expected_paragraph = OpenAcessParagraph(
        paragraph_id="Par10",
        section_id="Sec1",
        section_title="Introduction",
        text="It is of great significance to solve these shortcomings, and this paper proposed random undersampling for the majority categories samples and K-Smote oversampling for the minority categories samples to generate a more balanced data set. We also proposed the Self-Attention with Gate mechanism (SAG) to carry out feature extraction between the local and global features and filter irrelevant noise information for enhancing the generalization ability and calculating in parallel. The experimental results show that the precision is much higher than the comparison studies, especially the precision for the minority categories.",
    )
    assert expected_paragraph == article.paragraphs[0][4]
