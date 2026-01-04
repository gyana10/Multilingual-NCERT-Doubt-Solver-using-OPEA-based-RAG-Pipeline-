import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    TESTING = False
    
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
    
    TESSERACT_CMD = os.getenv('TESSERACT_CMD', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    TESSERACT_LANGUAGES = 'eng+hin+urd+tam+tel+ben+mar+guj+kan+mal'
    
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './embeddings')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'paraphrase-MiniLM-L6-v2')
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 512))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 50))
    TOP_K_RESULTS = int(os.getenv('TOP_K_RESULTS', 5))
    
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', 0.7))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 500))
    
    GRADES = list(range(5, 11))
    SUBJECTS = ['Math', 'Science', 'Social Science', 'English', 'Hindi']
    LANGUAGES = [
        'English', 'Hindi', 'Urdu', 'Tamil', 'Telugu', 
        'Bengali', 'Marathi', 'Gujarati', 'Kannada', 'Malayalam'
    ]
    
    RESPONSE_TIMEOUT = int(os.getenv('RESPONSE_TIMEOUT', 30))
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.1))
    
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}