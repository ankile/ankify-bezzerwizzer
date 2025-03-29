# Bezzerwizzer Anki Project Guidelines

## Commands
- Setup: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- Create folder: `python create_folder.py [--open]`
- Process images: `python process_images_to_csv.py <folder> --api-key <CLAUDE_API_KEY>`
- Test: `python -m pytest` (future; no tests implemented yet)
- Lint: `python -m flake8` (future; not configured yet)
- Type check: `python -m mypy process_images_to_csv.py create_folder.py`

## Code Style
- Formatting: Black compatible (single quotes for strings, 4 spaces for indentation)
- Imports: Group standard library, then third-party, then local imports
- Types: Use type hints for all function parameters and return values
- Naming: snake_case for variables/functions, PascalCase for classes
- Error handling: Use try/except blocks with specific exceptions
- Documentation: Docstrings for all functions and classes using """triple quotes"""
- JSON handling: Use indent=2 and ensure_ascii=False for output formatting
- CLI: Use argparse for command-line interfaces

## Project Structure
- `cards/`: Directory containing numbered folders (001, 002, etc.) with card images
- `create_folder.py`: Script to create a new numbered folder
- `process_images_to_csv.py`: Main script for processing images to CSV/JSON
- `requirements.txt`: Python dependencies

## Data Fields
- Question: The question text from the card
- Answer: The corresponding answer text
- Category: The Bezzerwizzer category (spaces replaced with underscores in CSV)
- CardID: Unique identifier for the card
- SourceFolder: Name of the folder containing the source images