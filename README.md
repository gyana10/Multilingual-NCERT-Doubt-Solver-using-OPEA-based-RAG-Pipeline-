# NCERT Doubt Solver

An AI-powered assistant that helps students find answers to their questions from official NCERT textbooks for classes 5-10.

## Features

- **NCERT Focused**: Answers based exclusively on official NCERT textbooks
- **Multilingual Support**: Get answers in multiple Indian languages
- **Smart Learning**: Step-by-step explanations with examples
- **Image Support**: Upload diagrams or math problems as images
- **Citations**: All answers include references to specific textbook pages
- **Confidence Scoring**: Each answer includes a confidence level indicator

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone or download this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install Tesseract OCR for image text extraction:
   - Windows: Download from [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`
   - Linux: `sudo apt install tesseract-ocr`

4. (Optional) Configure API keys in the `.env` file for LLM access

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

3. Ask questions about NCERT topics, upload images, and get AI-powered answers

## Project Structure

```
RAGNCERT/
├── app.py              # Main Flask application (Flask backend + HTML UI)
├── app_lite.py         # Alternate entrypoint (port 8000, imports app from app.py)
├── serve_frontend.py   # Helper to serve the standalone frontend (if used)
├── config.py           # Configuration settings and environment variables
├── simple_rag.py       # Default TF-IDF based RAG pipeline over NCERT chunks
├── opea_integration.py # FAISS / sentence-transformers based RAG pipeline (optional)
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
├── .gitignore          # Git ignore file
├── README.md           # This file
├── ARCHITECTURE.md     # Detailed system / RAG architecture notes
├── SETUP_GUIDE.md      # Additional setup instructions
├── chunks/             # Precomputed NCERT text chunks (class 5-10 *_chunks.jsonl)
├── embeddings/         # Vector DB / FAISS index files (if using OPEA pipeline)
├── templates/          # HTML templates (Flask UI)
│   └── index.html      # Main chat UI
├── frontend/           # Standalone frontend (if you prefer a separate UI)
├── uploads/            # Uploaded images (for OCR)
├── attachments/        # Design / integration helpers
├── database/           # SQLite DB and related helpers (if used)
└── utils/              # Utility modules (helpers, preprocessing, etc.)
```

## API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Process chat messages
- `POST /api/upload-image` - Handle image uploads for OCR
- `POST /api/feedback` - Submit feedback on answers
- `GET /api/conversation/<id>` - Retrieve conversation history
- `GET /api/languages` - Get supported languages
- `GET /api/subjects` - Get available subjects

## Configuration

The application can be configured using environment variables in the `.env` file:

- `FLASK_ENV`: Application environment (development/production)
- `SECRET_KEY`: Flask secret key
- `UPLOAD_FOLDER`: Directory for uploaded images
- `TESSERACT_CMD`: Path to Tesseract executable
- `LLM_PROVIDER`: LLM provider (openai, etc.)
- `OPENAI_API_KEY`: API key for OpenAI

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.