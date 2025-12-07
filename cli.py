#!/usr/bin/env python3
"""
Command-line interface for ebook management.
"""
import argparse
import sys
from ebook import Book
from storage import EbookStorage


def cmd_add(args, storage):
    """Add a new ebook to the collection."""
    book = Book(
        title=args.title,
        author=args.author,
        year=args.year,
        format=args.format,
        file_path=args.file,
        isbn=args.isbn
    )
    storage.add_book(book)
    print(f"Added: {book}")


def cmd_list(args, storage):
    """List all ebooks in the collection."""
    books = storage.load()
    if not books:
        print("No books in collection.")
        return
    
    print(f"Found {len(books)} book(s):\n")
    for i, book in enumerate(books):
        print(f"{i}: {book}")
        if args.verbose:
            if book.isbn:
                print(f"   ISBN: {book.isbn}")
            if book.file_path:
                print(f"   File: {book.file_path}")
            print()


def cmd_search(args, storage):
    """Search for ebooks by query."""
    results = storage.search_books_with_indices(args.query)
    if not results:
        print(f"No books found matching '{args.query}'.")
        return
    
    print(f"Found {len(results)} book(s) matching '{args.query}':\n")
    for index, book in results:
        print(f"{index}: {book}")


def cmd_delete(args, storage):
    """Delete an ebook from the collection."""
    book = storage.get_book(args.index)
    if not book:
        print(f"Error: No book at index {args.index}.")
        sys.exit(1)
    
    if storage.delete_book(args.index):
        print(f"Deleted: {book}")
    else:
        print(f"Error: Failed to delete book at index {args.index}.")
        sys.exit(1)


def cmd_show(args, storage):
    """Show detailed information about an ebook."""
    book = storage.get_book(args.index)
    if not book:
        print(f"Error: No book at index {args.index}.")
        sys.exit(1)
    
    print(f"Title:  {book.title}")
    print(f"Author: {book.author}")
    if book.year:
        print(f"Year:   {book.year}")
    if book.format:
        print(f"Format: {book.format}")
    if book.isbn:
        print(f"ISBN:   {book.isbn}")
    if book.file_path:
        print(f"File:   {book.file_path}")


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Manage your ebook collection",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--db',
        default='ebooks.json',
        help='Path to ebook database file (default: ebooks.json)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new ebook')
    add_parser.add_argument('title', help='Book title')
    add_parser.add_argument('author', help='Book author')
    add_parser.add_argument('--year', type=int, help='Publication year')
    add_parser.add_argument('--format', help='Book format (e.g., PDF, EPUB, MOBI)')
    add_parser.add_argument('--file', help='Path to ebook file')
    add_parser.add_argument('--isbn', help='ISBN number')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all ebooks')
    list_parser.add_argument('-v', '--verbose', action='store_true', 
                            help='Show detailed information')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for ebooks')
    search_parser.add_argument('query', help='Search query')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete an ebook')
    delete_parser.add_argument('index', type=int, help='Index of book to delete')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show ebook details')
    show_parser.add_argument('index', type=int, help='Index of book to show')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    storage = EbookStorage(args.db)
    
    commands = {
        'add': cmd_add,
        'list': cmd_list,
        'search': cmd_search,
        'delete': cmd_delete,
        'show': cmd_show
    }
    
    commands[args.command](args, storage)


if __name__ == '__main__':
    main()
