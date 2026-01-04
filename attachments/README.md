# NCERT Doubt-Solver - OPEA-based RAG System

## Project Overview
Multilingual NCERT Doubt-Solver using OPEA framework, Tesseract OCR, and Flask backend with RAG pipeline.

## Features
- ✅ Multilingual Q&A (10+ Indian languages)
- ✅ Grade-specific retrieval (Classes 5-10)
- ✅ Image-based question input with OCR
- ✅ Citation-backed answers
- ✅ Conversation history
- ✅ Student feedback system
- ✅ Voice input support
- ✅ Mobile-responsive design

## Tech Stack
- **Backend**: Flask, Python 3.9+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **OCR**: Tesseract OCR
- **RAG Framework**: OPEA
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers
- **LLM Integration**: OpenAI API (configurable)

## Installation

### Prerequisites
1. Python 3.9 or higher
2. Tesseract OCR installed
   - **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
   - **Linux**: `sudo apt-get install tesseract-ocr`
   - **Mac**: `brew install tesseract`

### Setup Steps

1. **Clone/Download the project**
   ```bash
   cd c:\Users\HP\intel
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Tesseract path** (Windows)
   - Open `app.py` and add Tesseract path:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

5. **Create .env file**
   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   OPENAI_API_KEY=your-openai-api-key
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the UI**
   Open browser: http://localhost:5000

## Project Structure
```
intel/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main UI template
├── static/
│   ├── css/
│   │   └── styles.css    # Styling
│   └── js/
│       └── app.js        # Frontend logic
├── uploads/              # Image uploads (auto-created)
└── README.md
```

## Usage Guide

### For Students:
1. Select your grade/class (5-10)
2. Choose subject (Math, Science, Social Science, etc.)
3. Select preferred language
4. Ask questions by:
   - Typing in the text box
   - Uploading image of question
   - Using voice input (click microphone icon)
5. View answers with citations
6. Rate answers to help improve the system

### API Endpoints

#### Chat Endpoint
```
POST /api/chat
Content-Type: application/json

{
  "message": "What is photosynthesis?",
  "grade": 8,
  "subject": "Science",
  "language": "English",
  "conversation_id": "optional-uuid"
}
```

#### Image Upload
```
POST /api/upload-image
Content-Type: multipart/form-data

Form data:
- image: <file>
```

#### Submit Feedback
```
POST /api/feedback
Content-Type: application/json

{
  "conversation_id": "uuid",
  "message_index": 0,
  "rating": 5,
  "comment": "Very helpful!"
}
```

## Integration Points

### OPEA RAG Pipeline Integration
The UI is designed to work with OPEA framework. To integrate:

1. **Update `/api/chat` endpoint in app.py**:
   ```python
   # Import your OPEA RAG pipeline
   from opea_pipeline import RAGPipeline
   
   rag = RAGPipeline()
   
   @app.route('/api/chat', methods=['POST'])
   def chat():
       data = request.json
       # Use OPEA pipeline
       result = rag.query(
           question=data['message'],
           grade=data['grade'],
           subject=data['subject'],
           language=data['language']
       )
       return jsonify(result)
   ```

2. **Update OCR processing**:
   ```python
   import pytesseract
   from PIL import Image
   
   @app.route('/api/upload-image', methods=['POST'])
   def upload_image():
       file = request.files['image']
       image = Image.open(file)
       text = pytesseract.image_to_string(image, lang='eng+hin')
       return jsonify({'extracted_text': text})
   ```

## Performance Optimization
- Implement caching for frequent queries
- Use async processing for OCR
- Optimize vector search with proper indexing
- Implement rate limiting
- Add CDN for static assets

## Mobile Responsiveness
The UI is fully responsive and works on:
- Desktop browsers (Chrome, Firefox, Edge, Safari)
- Tablets (iPad, Android tablets)
- Mobile phones (iOS, Android)

## Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Next Steps for Production

1. **Database Integration**: Replace in-memory storage with PostgreSQL/MongoDB
2. **OPEA Pipeline**: Integrate actual RAG pipeline
3. **Vector DB**: Connect ChromaDB with NCERT embeddings
4. **Authentication**: Add user login/signup
5. **Analytics**: Track usage patterns
6. **Deployment**: Deploy on cloud (AWS/Azure/GCP)
7. **Testing**: Add unit and integration tests
8. **CI/CD**: Setup automated deployment

## License
Educational project for NCERT Doubt-Solver system.

## Support
For issues and questions, please refer to project documentation.
