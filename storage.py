"""
Storage layer for ebook collection.
"""
import json
import os
from typing import List, Optional, Tuple
from ebook import Book


class EbookStorage:
    """Handles persistence of ebook collection."""
    
    def __init__(self, filepath: str = "ebooks.json"):
        """Initialize storage with a file path."""
        self.filepath = filepath
    
    def load(self) -> List[Book]:
        """Load books from storage."""
        if not os.path.exists(self.filepath):
            return []
        
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                return [Book.from_dict(book) for book in data]
        except (json.JSONDecodeError, KeyError):
            return []
    
    def save(self, books: List[Book]) -> None:
        """Save books to storage."""
        with open(self.filepath, 'w') as f:
            data = [book.to_dict() for book in books]
            json.dump(data, f, indent=2)
    
    def add_book(self, book: Book) -> None:
        """Add a book to the collection."""
        books = self.load()
        books.append(book)
        self.save(books)
    
    def delete_book(self, index: int) -> bool:
        """Delete a book by index."""
        books = self.load()
        if 0 <= index < len(books):
            books.pop(index)
            self.save(books)
            return True
        return False
    
    def search_books(self, query: str) -> List[Book]:
        """Search books by query."""
        books = self.load()
        return [book for book in books if book.matches_query(query)]
    
    def search_books_with_indices(self, query: str) -> List[Tuple[int, Book]]:
        """Search books by query and return list of (index, book) tuples."""
        books = self.load()
        return [(i, book) for i, book in enumerate(books) if book.matches_query(query)]
    
    def get_book(self, index: int) -> Optional[Book]:
        """Get a book by index."""
        books = self.load()
        if 0 <= index < len(books):
            return books[index]
        return None
