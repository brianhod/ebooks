# Ebooks Manager

A simple command-line tool for managing your ebook collection.

## Features

- Add ebooks with metadata (title, author, year, format, ISBN, file path)
- List all ebooks in your collection
- Search for ebooks by any field
- Delete ebooks from your collection
- View detailed information about specific ebooks
- JSON-based storage for easy backup and portability

## Installation

1. Clone the repository:
```bash
git clone https://github.com/brianhod/ebooks.git
cd ebooks
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The ebooks manager provides several commands to manage your collection:

### Add a Book

```bash
python cli.py add "Book Title" "Author Name" [options]
```

Options:
- `--year YEAR`: Publication year
- `--format FORMAT`: Book format (e.g., PDF, EPUB, MOBI)
- `--file PATH`: Path to the ebook file
- `--isbn ISBN`: ISBN number

Example:
```bash
python cli.py add "Python Programming" "John Doe" --year 2023 --format PDF --isbn 978-1234567890
```

### List Books

```bash
python cli.py list [-v]
```

Use `-v` or `--verbose` for detailed information including ISBN and file paths.

Example:
```bash
python cli.py list
python cli.py list -v
```

### Search Books

```bash
python cli.py search "query"
```

Search across all fields (title, author, year, format, ISBN).

Example:
```bash
python cli.py search "python"
python cli.py search "2023"
```

### Show Book Details

```bash
python cli.py show INDEX
```

Display detailed information about a specific book by its index.

Example:
```bash
python cli.py show 0
```

### Delete a Book

```bash
python cli.py delete INDEX
```

Remove a book from the collection by its index.

Example:
```bash
python cli.py delete 0
```

### Custom Database File

By default, books are stored in `ebooks.json`. You can specify a different file:

```bash
python cli.py --db my-books.json list
```

## Development

### Running Tests

```bash
pytest
```

### Running Tests with Coverage

```bash
pytest --cov=. --cov-report=html
```

## Data Storage

Books are stored in a JSON file (`ebooks.json` by default). The file is human-readable and can be easily backed up or edited manually if needed.

Example storage format:
```json
[
  {
    "title": "Python Programming",
    "author": "John Doe",
    "year": 2023,
    "format": "PDF",
    "file_path": "/path/to/book.pdf",
    "isbn": "978-1234567890"
  }
]
```

## License

This project is open source and available under the MIT License.
