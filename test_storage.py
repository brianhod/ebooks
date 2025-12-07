"""
Tests for storage module.
"""
import os
import tempfile
import pytest
from ebook import Book
from storage import EbookStorage


@pytest.fixture
def temp_storage():
    """Create a temporary storage file."""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    storage = EbookStorage(path)
    yield storage
    if os.path.exists(path):
        os.unlink(path)


def test_storage_load_empty(temp_storage):
    """Test loading from non-existent file."""
    books = temp_storage.load()
    assert books == []


def test_storage_save_and_load(temp_storage):
    """Test saving and loading books."""
    books = [
        Book(title="Book 1", author="Author 1"),
        Book(title="Book 2", author="Author 2", year=2023)
    ]
    temp_storage.save(books)
    loaded = temp_storage.load()
    
    assert len(loaded) == 2
    assert loaded[0].title == "Book 1"
    assert loaded[1].title == "Book 2"
    assert loaded[1].year == 2023


def test_storage_add_book(temp_storage):
    """Test adding a book."""
    book = Book(title="Test Book", author="Test Author")
    temp_storage.add_book(book)
    
    books = temp_storage.load()
    assert len(books) == 1
    assert books[0].title == "Test Book"


def test_storage_add_multiple_books(temp_storage):
    """Test adding multiple books."""
    temp_storage.add_book(Book(title="Book 1", author="Author 1"))
    temp_storage.add_book(Book(title="Book 2", author="Author 2"))
    
    books = temp_storage.load()
    assert len(books) == 2


def test_storage_delete_book(temp_storage):
    """Test deleting a book."""
    temp_storage.add_book(Book(title="Book 1", author="Author 1"))
    temp_storage.add_book(Book(title="Book 2", author="Author 2"))
    
    result = temp_storage.delete_book(0)
    assert result is True
    
    books = temp_storage.load()
    assert len(books) == 1
    assert books[0].title == "Book 2"


def test_storage_delete_invalid_index(temp_storage):
    """Test deleting with invalid index."""
    temp_storage.add_book(Book(title="Book 1", author="Author 1"))
    
    result = temp_storage.delete_book(5)
    assert result is False
    
    books = temp_storage.load()
    assert len(books) == 1


def test_storage_search_books(temp_storage):
    """Test searching books."""
    temp_storage.add_book(Book(title="Python Programming", author="John Doe"))
    temp_storage.add_book(Book(title="Java Basics", author="Jane Smith"))
    temp_storage.add_book(Book(title="Advanced Python", author="Bob Johnson"))
    
    results = temp_storage.search_books("python")
    assert len(results) == 2
    assert all("Python" in book.title for book in results)


def test_storage_search_no_results(temp_storage):
    """Test searching with no matches."""
    temp_storage.add_book(Book(title="Python Programming", author="John Doe"))
    
    results = temp_storage.search_books("rust")
    assert len(results) == 0


def test_storage_get_book(temp_storage):
    """Test getting a book by index."""
    temp_storage.add_book(Book(title="Book 1", author="Author 1"))
    temp_storage.add_book(Book(title="Book 2", author="Author 2"))
    
    book = temp_storage.get_book(1)
    assert book is not None
    assert book.title == "Book 2"


def test_storage_get_book_invalid_index(temp_storage):
    """Test getting book with invalid index."""
    temp_storage.add_book(Book(title="Book 1", author="Author 1"))
    
    book = temp_storage.get_book(5)
    assert book is None


def test_storage_get_book_negative_index(temp_storage):
    """Test getting book with negative index."""
    temp_storage.add_book(Book(title="Book 1", author="Author 1"))
    
    book = temp_storage.get_book(-1)
    assert book is None
