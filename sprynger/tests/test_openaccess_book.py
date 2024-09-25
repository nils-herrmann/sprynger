"""Tests for the OpenAccessBook class."""
import pytest

from sprynger import init
from sprynger import OpenAccessBook, OpenAccessChapter
from sprynger.openaccess_book import _Chapter
from sprynger.utils.data_structures import BookMeta, ChapterMeta, OpenAcessParagraph

init()

book = OpenAccessBook("978-3-031-63500-7", start=1, nr_results=2, refresh=30)
chapter = OpenAccessChapter("10.1007/978-3-031-61874-1_5", refresh=30)
chapter_with_text = OpenAccessChapter("10.1007/978-3-031-24498-8_7", refresh=30)
with pytest.warns(UserWarning):
    book_pagination = OpenAccessBook('978-3-031-63498-7', nr_results=30, refresh=30)

def test_book_meta():
    """Test the book meta data."""
    book_expected_meta = BookMeta(
        doi="10.1007/978-3-031-63501-4",
        publisher_id="978-3-031-63501-4",
        book_title_id="631234",
        pub_date="2024-01-01",
        isbn_print="978-3-031-63500-7",
        isbn_electronic="978-3-031-63501-4",
        publisher_name="Springer Nature Switzerland",
        publisher_loc="Cham",
    )
    assert book.metadata == book_expected_meta

    chapter_expected_meta = BookMeta(
        doi="10.1007/978-3-031-61874-1",
        publisher_id="978-3-031-61874-1",
        book_title_id="514295",
        pub_date="2024-01-01",
        isbn_print="978-3-031-61873-4",
        isbn_electronic="978-3-031-61874-1",
        publisher_name="Springer International Publishing",
        publisher_loc="Cham",
    )
    assert chapter.book_metadata == chapter_expected_meta


def test_chapter_meta():
    """Test the chapter meta data."""
    chapter_expected_meta = ChapterMeta(doi='10.1007/978-3-031-61874-1_5',
                                        chapter='5')
    assert chapter.metadata == chapter_expected_meta

    assert isinstance(book[0].metadata, ChapterMeta)


def test_iterable():
    """Test the lengths of the book and the chapters."""
    assert len(book) == 2
    for book_chapter in book:
        assert isinstance(book_chapter, _Chapter)


def test_paragraphs():
    """Test the paragraphs."""
    assert chapter.paragraphs == []

    assert len(chapter_with_text.paragraphs) == 41
    expected_paragraph = OpenAcessParagraph(
        paragraph_id="Par6",
        section_id="Sec1",
        section_title="Introduction",
        text="Research Question: What are the salient points that Data Scientists should be aware of when it comes to Data Governance within organizations?",
    )
    assert chapter_with_text.paragraphs[4] == expected_paragraph


def test_pagination():
    """Test the pagination."""
    assert len(book_pagination) == 27
    dois = set([chapter.metadata.doi for chapter in book_pagination])
    assert len(dois) == 27


def test_warning():
    """Test warning message."""
    w_message = r'Too many results requested\. 27 document\(s\) found but 30 requested\.'
    with pytest.warns(UserWarning, match=w_message):
        OpenAccessBook('978-3-031-63498-7', nr_results=30, refresh=30)
