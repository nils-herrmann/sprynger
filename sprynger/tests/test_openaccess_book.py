"""Tests for the OpenAccessBook class."""
from sprynger import init
from sprynger import OpenAccessBook
from sprynger.utils.data_structures import BookMeta, ChapterMeta, OpenAcessParagraph

init()

book = OpenAccessBook("978-3-031-63500-7", start=1, max_results=2, refresh=30)
chapter = OpenAccessBook("10.1007/978-3-031-61874-1_5", refresh=30)
chapter_with_text = OpenAccessBook("10.1007/978-3-031-24498-8_7", refresh=30)

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
    assert book.book_meta == book_expected_meta

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
    assert chapter.book_meta == chapter_expected_meta


def test_chapter_meta():
    """Test the chapter meta data."""
    assert len(book.chapter_meta) == 4

    assert len(chapter.chapter_meta) == 1
    assert chapter.chapter_meta == [
        ChapterMeta(doi="10.1007/978-3-031-61874-1_5", chapter="5")
    ]


def test_paragraphs():
    """Test the paragraphs."""
    assert chapter.paragraphs == [[]]

    assert len(chapter_with_text.paragraphs[0]) == 41
    expected_paragraph = OpenAcessParagraph(
        paragraph_id="Par6",
        section_id="Sec1",
        section_title="Introduction",
        text="Research Question: What are the salient points that Data Scientists should be aware of when it comes to Data Governance within organizations?",
    )
    assert chapter_with_text.paragraphs[0][4] == expected_paragraph
