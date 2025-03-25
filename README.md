# Local LLM with Vector DB

A Python application that combines OpenAI's API with ChromaDB for document querying and AI-enhanced responses. This project allows you to load documents (including Excel files), store them in a vector database, and query them using natural language with AI-powered responses.

## Features

- 🤖 Integration with OpenAI's API for LLM capabilities and embeddings
- 📚 ChromaDB vector database for efficient document storage and retrieval
- 📄 Support for multiple document formats:
  - Excel files (.xlsx)
  - PDF documents
  - Word documents (.docx)
  - HTML files
  - Text files (.txt)
- 🔍 Natural language querying of documents
- 🎯 AI-enhanced responses based on document context
- 📊 Special handling for Excel files with metadata extraction

## Prerequisites

- Python 3.8+
- OpenAI API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Local-LLM-with-vector-db.git
cd Local-LLM-with-vector-db
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following content:
```
OPENAI_API_KEY=your_api_key_here
DEFAULT_CHATGPT_MODEL=gpt-3.5-turbo
DEFAULT_EMBEDDING_MODEL=text-embedding-3-small
```

## Usage

1. Place your documents in the `docs` directory
2. Run the application:
```bash
python main.py
```

The application will:
1. Load and process all documents in the `docs` directory
2. Create embeddings using OpenAI's embedding model
3. Store documents and embeddings in ChromaDB
4. Allow you to query the documents using natural language
5. Provide AI-enhanced responses based on the document context

## Project Structure

- `main.py` - Main application file with OpenAI API integration and ChromaDB setup
- `doc_loader.py` - Document loading and processing utilities for various file formats
- `excel_functions.py` - Specialized functions for Excel file processing
- `docs/` - Directory for storing documents to be processed
- `.env` - Environment configuration
- `requirements.txt` - Python dependencies

## Document Processing

The application handles different document types:
- Excel files: Processes each row with metadata extraction
- PDF files: Extracts text from all pages
- Word documents: Processes paragraphs
- HTML files: Extracts text content
- Text files: Direct text processing

## License

MIT License 