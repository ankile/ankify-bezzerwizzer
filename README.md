# Bezzerwizzer Anki

A tool to convert Bezzerwizzer trivia card images into Anki flashcards.

## Overview

This tool processes pairs of Bezzerwizzer card images (question and answer images) and converts them into Anki-compatible CSV files for import into Anki. It uses Anthropic's Claude API to extract question-answer pairs from the images.

## Requirements

- Python 3.8+
- Anthropic API key

## Installation

1. Clone this repository
2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. Add your Anthropic API key to the `.env` file:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

2. Create a new timestamped folder for your images:
   ```bash
   python create_folder.py
   # Or to open the folder after creation:
   python create_folder.py --open
   ```

3. Copy your image pairs to the created folder

4. Process the images:
   ```bash
   python process_images_to_csv.py path/to/folder
   ```

Optional arguments:
- `--api-key <YOUR_CLAUDE_API_KEY>`: Override the API key from .env file
- `--output-csv <filename>`: Specify custom output CSV filename (default: saves to input folder as "bezzerwizzer_anki.csv")
- `--output-json <filename>`: Specify custom output JSON filename (default: saves to input folder as "bezzerwizzer_cards.json")

### Image Requirements

- Images should be organized in pairs (question image followed by answer image)
- Supported formats: JPG, JPEG, PNG

## Output

- CSV file compatible with Anki import
- JSON file with all extracted question-answer pairs