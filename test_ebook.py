"""
Tests for ebook module.
"""
import pytest
from ebook import Book


def test_book_creation():
    """Test creating a book with basic fields."""
    book = Book(title="Test Book", author="Test Author")
    assert book.title == "Test Book"
    assert book.author == "Test Author"


def test_book_with_all_fields():
    """Test creating a book with all fields."""
    book = Book(
        title="Complete Book",
        author="Complete Author",
        year=2023,
        format="PDF",
        file_path="/path/to/book.pdf",
        isbn="123-456-789"
    )
    assert book.title == "Complete Book"
    assert book.author == "Complete Author"
    assert book.year == 2023
    assert book.format == "PDF"
    assert book.file_path == "/path/to/book.pdf"
    assert book.isbn == "123-456-789"


def test_book_to_dict():
    """Test converting book to dictionary."""
    book = Book(title="Test", author="Author", year=2023)
    data = book.to_dict()
    assert data["title"] == "Test"
    assert data["author"] == "Author"
    assert data["year"] == 2023


def test_book_from_dict():
    """Test creating book from dictionary."""
    data = {
        "title": "Test",
        "author": "Author",
        "year": 2023,
        "format": None,
        "file_path": None,
        "isbn": None
    }
    book = Book.from_dict(data)
    assert book.title == "Test"
    assert book.author == "Author"
    assert book.year == 2023


def test_book_matches_query_title():
    """Test searching by title."""
    book = Book(title="Python Programming", author="John Doe")
    assert book.matches_query("python")
    assert book.matches_query("Programming")
    assert not book.matches_query("java")


def test_book_matches_query_author():
    """Test searching by author."""
    book = Book(title="Test Book", author="John Doe")
    assert book.matches_query("john")
    assert book.matches_query("doe")
    assert not book.matches_query("smith")


def test_book_matches_query_year():
    """Test searching by year."""
    book = Book(title="Test", author="Author", year=2023)
    assert book.matches_query("2023")
    assert not book.matches_query("2022")


def test_book_matches_query_case_insensitive():
    """Test case-insensitive searching."""
    book = Book(title="Python Programming", author="John Doe")
    assert book.matches_query("PYTHON")
    assert book.matches_query("python")
    assert book.matches_query("Python")


def test_book_str_basic():
    """Test string representation with basic fields."""
    book = Book(title="Test Book", author="Test Author")
    assert '"Test Book" by Test Author' in str(book)


def test_book_str_with_year():
    """Test string representation with year."""
    book = Book(title="Test Book", author="Test Author", year=2023)
    result = str(book)
    assert "Test Book" in result
    assert "Test Author" in result
    assert "(2023)" in result


def test_book_str_with_format():
    """Test string representation with format."""
    book = Book(title="Test Book", author="Test Author", format="PDF")
    result = str(book)
    assert "Test Book" in result
    assert "[PDF]" in result
