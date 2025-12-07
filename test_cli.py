"""
Tests for CLI module.
"""
import os
import tempfile
import pytest
from io import StringIO
from unittest.mock import patch
from ebook import Book
from storage import EbookStorage
import cli


@pytest.fixture
def temp_storage():
    """Create a temporary storage file."""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    storage = EbookStorage(path)
    yield storage, path
    if os.path.exists(path):
        os.unlink(path)


def test_cmd_add(temp_storage):
    """Test add command."""
    storage, _ = temp_storage
    
    class Args:
        title = "Test Book"
        author = "Test Author"
        year = 2023
        format = "PDF"
        file = "/test/path"
        isbn = "123-456"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.cmd_add(Args(), storage)
        output = fake_out.getvalue()
        assert "Added:" in output
        assert "Test Book" in output
    
    books = storage.load()
    assert len(books) == 1
    assert books[0].title == "Test Book"


def test_cmd_list_empty(temp_storage):
    """Test list command with empty collection."""
    storage, _ = temp_storage
    
    class Args:
        verbose = False
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.cmd_list(Args(), storage)
        output = fake_out.getvalue()
        assert "No books in collection" in output


def test_cmd_list_with_books(temp_storage):
    """Test list command with books."""
    storage, _ = temp_storage
    storage.add_book(Book(title="Book 1", author="Author 1"))
    storage.add_book(Book(title="Book 2", author="Author 2"))
    
    class Args:
        verbose = False
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.cmd_list(Args(), storage)
        output = fake_out.getvalue()
        assert "Found 2 book(s)" in output
        assert "Book 1" in output
        assert "Book 2" in output


def test_cmd_list_verbose(temp_storage):
    """Test list command with verbose output."""
    storage, _ = temp_storage
    storage.add_book(Book(
        title="Book 1",
        author="Author 1",
        isbn="123-456",
        file_path="/path/to/book"
    ))
    
    class Args:
        verbose = True
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.cmd_list(Args(), storage)
        output = fake_out.getvalue()
        assert "ISBN: 123-456" in output
        assert "File: /path/to/book" in output


def test_cmd_search_found(temp_storage):
    """Test search command with results."""
    storage, _ = temp_storage
    storage.add_book(Book(title="Python Programming", author="John Doe"))
    storage.add_book(Book(title="Java Basics", author="Jane Smith"))
    
    class Args:
        query = "python"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.cmd_search(Args(), storage)
        output = fake_out.getvalue()
        assert "Found 1 book(s)" in output
        assert "Python Programming" in output


def test_cmd_search_not_found(temp_storage):
    """Test search command with no results."""
    storage, _ = temp_storage
    storage.add_book(Book(title="Python Programming", author="John Doe"))
    
    class Args:
        query = "rust"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.cmd_search(Args(), storage)
        output = fake_out.getvalue()
        assert "No books found" in output


def test_cmd_delete_success(temp_storage):
    """Test delete command."""
    storage, _ = temp_storage
    storage.add_book(Book(title="Book to Delete", author="Author"))
    
    class Args:
        index = 0
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.cmd_delete(Args(), storage)
        output = fake_out.getvalue()
        assert "Deleted:" in output
        assert "Book to Delete" in output
    
    books = storage.load()
    assert len(books) == 0


def test_cmd_delete_invalid_index(temp_storage):
    """Test delete command with invalid index."""
    storage, _ = temp_storage
    
    class Args:
        index = 5
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with pytest.raises(SystemExit):
            cli.cmd_delete(Args(), storage)


def test_cmd_show(temp_storage):
    """Test show command."""
    storage, _ = temp_storage
    storage.add_book(Book(
        title="Test Book",
        author="Test Author",
        year=2023,
        format="PDF",
        isbn="123-456",
        file_path="/path/to/book"
    ))
    
    class Args:
        index = 0
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        cli.cmd_show(Args(), storage)
        output = fake_out.getvalue()
        assert "Title:  Test Book" in output
        assert "Author: Test Author" in output
        assert "Year:   2023" in output
        assert "Format: PDF" in output
        assert "ISBN:   123-456" in output
        assert "File:   /path/to/book" in output


def test_cmd_show_invalid_index(temp_storage):
    """Test show command with invalid index."""
    storage, _ = temp_storage
    
    class Args:
        index = 5
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with pytest.raises(SystemExit):
            cli.cmd_show(Args(), storage)
