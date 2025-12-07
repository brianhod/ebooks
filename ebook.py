"""
Ebook data model and representation.
"""
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Book:
    """Represents an ebook with metadata."""
    title: str
    author: str
    year: Optional[int] = None
    format: Optional[str] = None
    file_path: Optional[str] = None
    isbn: Optional[str] = None
    
    def to_dict(self):
        """Convert book to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        """Create book from dictionary."""
        return cls(**data)
    
    def matches_query(self, query: str) -> bool:
        """Check if book matches a search query."""
        query_lower = query.lower()
        fields = [
            self.title.lower() if self.title else "",
            self.author.lower() if self.author else "",
            str(self.year) if self.year else "",
            self.format.lower() if self.format else "",
            self.isbn if self.isbn else ""
        ]
        return any(query_lower in field for field in fields)
    
    def __str__(self):
        """String representation of the book."""
        parts = [f'"{self.title}" by {self.author}']
        if self.year:
            parts.append(f"({self.year})")
        if self.format:
            parts.append(f"[{self.format}]")
        return " ".join(parts)
