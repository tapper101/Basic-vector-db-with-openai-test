# Local Vector DB Project

A Python application that combines Ollama LLM with ChromaDB for document querying and AI-enhanced responses. This project allows you to load documents (including Excel files), store them in a vector database, and query them using natural language with AI-powered responses.

## Features

- 🤖 Integration with Ollama for LLM capabilities
- 📚 ChromaDB vector database for efficient document storage and retrieval
- 📄 Support for multiple document formats including Excel files
- 🔍 Natural language querying of documents
- 🎯 AI-enhanced responses based on document context

## Prerequisites

- Python 3.8+
- Ollama running locally (default: http://localhost:11434)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Local-vector-DB-project.git
cd Local-vector-DB-project
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

4. Make sure Ollama is running locally and the required models are installed:
```bash
ollama pull llama2
ollama pull nomic-embed-text
```

## Configuration

Create a `.env` file in the project root with the following content:
```
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama2
```

## Usage

1. Place your documents in the `docs` directory
2. Run the application:
```bash
python main.py
```

The application will:
1. Load and process all documents in the `docs` directory
2. Create embeddings using Ollama
3. Store documents and embeddings in ChromaDB
4. Allow you to query the documents using natural language
5. Provide AI-enhanced responses based on the document context

## Project Structure

- `main.py` - Main application file
- `doc_loader.py` - Document loading and processing utilities
- `docs/` - Directory for storing documents to be processed
- `.env` - Environment configuration
- `requirements.txt` - Python dependencies

## License

MIT License 