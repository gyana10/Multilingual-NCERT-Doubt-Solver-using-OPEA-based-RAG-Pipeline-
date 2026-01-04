# Complete Setup Guide - NCERT Doubt-Solver

## System Requirements

### Hardware
- **Minimum**: 8GB RAM, 4 CPU cores
- **Recommended**: 16GB RAM, 8 CPU cores (for optimal performance)
- **Storage**: 10GB free space (for NCERT PDFs and vector database)

### Software
- **OS**: Windows 10/11, Linux, or macOS
- **Python**: 3.9 or higher
- **Tesseract OCR**: Latest version
- **Browser**: Chrome 90+, Firefox 88+, Edge 90+, or Safari 14+

## Step-by-Step Installation

### 1. Install Python
Download and install Python 3.9+ from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
```

### 2. Install Tesseract OCR

#### Windows:
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (default location: `C:\Program Files\Tesseract-OCR\`)
3. Add to PATH or configure in `config.py`

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-hin tesseract-ocr-tam  # Additional languages
```

#### macOS:
```bash
brew install tesseract
brew install tesseract-lang  # For additional languages
```

Verify installation:
```bash
tesseract --version
```

### 3. Clone/Setup Project

Navigate to project directory:
```bash
cd c:\Users\HP\intel
```

### 4. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### 5. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-CORS (cross-origin support)
- Pillow (image processing)
- pytesseract (OCR integration)
- langchain (LLM framework)
- sentence-transformers (embeddings)
- chromadb (vector database)
- and other dependencies

### 6. Configure Environment

Create `.env` file from template:
```bash
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac
```

Edit `.env` file and configure:
```env
# Flask settings
FLASK_ENV=development
SECRET_KEY=your-unique-secret-key-here

# Tesseract path (Windows - adjust if different)
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# OpenAI API (if using GPT models)
OPENAI_API_KEY=your-openai-api-key

# Or use local models (recommended for privacy)
LLM_PROVIDER=local
LLM_MODEL=llama2  # or other local model
```

### 7. Configure Tesseract Path (Windows Only)

If Tesseract is installed in a different location, update `config.py`:
```python
TESSERACT_CMD = r'C:\Your\Custom\Path\tesseract.exe'
```

### 8. Create Required Directories

```bash
mkdir uploads
mkdir vector_db
mkdir data
```

## Running the Application

### Quick Start (Windows)

Simply double-click `run.bat` or execute:
```bash
.\run.bat
```

### Manual Start

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run Flask app
python app.py
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

For mobile testing, use your computer's IP:
```
http://192.168.x.x:5000
```

## OPEA RAG Pipeline Integration

The current implementation includes placeholder functions. To integrate actual OPEA components:

### 1. Install OPEA Framework

```bash
pip install opea-framework  # Replace with actual OPEA package
```

### 2. Update `opea_integration.py`

Implement the following methods with actual OPEA components:

- `_initialize_vector_db()`: Connect to ChromaDB/FAISS
- `_initialize_embedding_model()`: Load embedding model
- `_initialize_llm()`: Configure LLM (OpenAI/local)
- `_retrieve_documents()`: Vector similarity search
- `_generate_answer()`: LLM-based generation

### 3. Ingest NCERT Documents

Place NCERT PDFs in the `data/` directory:
```
data/
├── class_5/
│   ├── math.pdf
│   ├── science.pdf
├── class_6/
│   ├── math.pdf
│   ├── science.pdf
...
```

Run ingestion script (to be created):
```bash
python scripts/ingest_ncert.py
```

## Testing

### Test OCR Functionality

Upload a test image through the UI or use API:
```bash
curl -X POST http://localhost:5000/api/upload-image \
  -F "image=@test_image.jpg"
```

### Test Chat API

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is photosynthesis?",
    "grade": 8,
    "subject": "Science",
    "language": "English"
  }'
```

### Test Feedback

```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test-123",
    "message_index": 0,
    "rating": 5,
    "comment": "Great answer!"
  }'
```

## Troubleshooting

### Issue: Tesseract not found

**Solution**: 
- Verify Tesseract installation: `tesseract --version`
- Update `TESSERACT_CMD` in `config.py` with correct path
- Ensure Tesseract is in system PATH

### Issue: Module import errors

**Solution**:
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Port 5000 already in use

**Solution**:
Change port in `app.py`:
```python
app.run(port=5001)  # Use different port
```

### Issue: CORS errors in browser

**Solution**: Already configured in `app.py`, but verify CORS is enabled

### Issue: Large file upload fails

**Solution**: Increase max size in `config.py`:
```python
MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB
```

## Performance Optimization

### 1. Use Production Server

For production, use Gunicorn (Linux/Mac) or Waitress (Windows):

```bash
# Install
pip install gunicorn  # Linux/Mac
pip install waitress  # Windows

# Run
gunicorn -w 4 -b 0.0.0.0:5000 app:app  # Linux/Mac
waitress-serve --host=0.0.0.0 --port=5000 app:app  # Windows
```

### 2. Enable Caching

Add Redis caching for frequent queries:
```bash
pip install redis flask-caching
```

### 3. Database Setup

Replace in-memory storage with PostgreSQL/MongoDB:
```bash
pip install psycopg2-binary  # PostgreSQL
pip install pymongo  # MongoDB
```

### 4. Use CDN

For production, serve static files via CDN for better performance.

## Security Checklist

- [ ] Change default SECRET_KEY in production
- [ ] Enable HTTPS (use SSL certificate)
- [ ] Add rate limiting (flask-limiter)
- [ ] Implement user authentication
- [ ] Validate and sanitize all inputs
- [ ] Set up proper CORS policies
- [ ] Use environment variables for sensitive data
- [ ] Regular security updates

## Deployment Options

### Option 1: Docker (Recommended)

Create `Dockerfile` and `docker-compose.yml` for containerized deployment.

### Option 2: Cloud Platforms

- **AWS**: EC2, Elastic Beanstalk, or Lambda
- **Azure**: App Service or Container Instances
- **Google Cloud**: App Engine or Cloud Run
- **Heroku**: Easy deployment with buildpacks

### Option 3: Traditional VPS

Deploy on DigitalOcean, Linode, or similar VPS providers.

## Monitoring & Logging

### Setup Logging

Logs are configured in `app.py`. View logs:
```bash
tail -f app.log  # Linux/Mac
Get-Content app.log -Wait  # Windows PowerShell
```

### Performance Monitoring

Consider adding:
- **Application Performance Monitoring (APM)**: New Relic, DataDog
- **Error Tracking**: Sentry
- **Analytics**: Google Analytics, Mixpanel

## Next Steps

1. **Integrate OPEA RAG Pipeline**: Implement actual document retrieval and answer generation
2. **Add Authentication**: User login/registration system
3. **Database Integration**: PostgreSQL for conversations and feedback
4. **Fine-tune LLM**: Train model on regional languages
5. **Create Evaluation Dataset**: Test accuracy and quality
6. **Performance Optimization**: Caching, query optimization
7. **Mobile App**: React Native or Flutter app
8. **Voice I/O**: Integrate speech-to-text and text-to-speech

## Support & Resources

- **OPEA Documentation**: [Link to OPEA docs]
- **Tesseract OCR**: https://github.com/tesseract-ocr/tesseract
- **Flask Documentation**: https://flask.palletsprojects.com/
- **LangChain**: https://python.langchain.com/

## License

Educational project for NCERT Doubt-Solver system.

---

For issues or questions, please refer to project documentation or contact the development team.
