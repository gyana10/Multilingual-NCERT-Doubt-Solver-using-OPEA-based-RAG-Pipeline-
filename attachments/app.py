from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from datetime import datetime
import uuid
import logging
from config import config
from opea_integration import get_rag_pipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

app.secret_key = app.config['SECRET_KEY']
CORS(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

try:
    rag_pipeline = get_rag_pipeline()
    logger.info("RAG pipeline initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG pipeline: {e}")
    rag_pipeline = None

conversations = {}
feedback_data = []

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Handle chat messages
    Expected JSON: {
        'message': str,
        'grade': int,
        'subject': str,
        'language': str,
        'conversation_id': str (optional),
        'image_text': str (optional)
    }
    """
    try:
        data = request.json
        message = data.get('message', '')
        image_text = data.get('image_text', '')
        
        full_message = f"{message}\n\n{image_text}" if image_text else message
        
        grade = data.get('grade', 8)
        subject = data.get('subject', 'Math')
        language = data.get('language', 'English')
        conversation_id = data.get('conversation_id', str(uuid.uuid4()))
        
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        conversations[conversation_id].append({
            'role': 'user',
            'message': full_message,
            'timestamp': datetime.now().isoformat()
        })
        
        if rag_pipeline:
            try:
                result = rag_pipeline.query(
                    question=full_message,
                    grade=grade,
                    subject=subject,
                    language=language,
                    conversation_history=conversations[conversation_id][:-1]
                )
                
                response = {
                    'conversation_id': conversation_id,
                    'answer': result['answer'],
                    'citations': result['citations'],
                    'confidence': result['confidence'],
                    'language': result['language'],
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                logger.error(f"RAG pipeline error: {e}")
                response = _generate_placeholder_response(
                    conversation_id, grade, subject, language
                )
        else:
            response = _generate_placeholder_response(
                conversation_id, grade, subject, language
            )
        
        conversations[conversation_id].append({
            'role': 'assistant',
            'message': response['answer'],
            'citations': response['citations'],
            'timestamp': response['timestamp']
        })
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500


def _generate_placeholder_response(conversation_id, grade, subject, language):
    """Generate placeholder response when RAG pipeline is unavailable"""
    return {
        'conversation_id': conversation_id,
        'answer': f"This is a placeholder response. To get actual answers from NCERT textbooks, please integrate the OPEA RAG pipeline. (Grade: {grade}, Subject: {subject}, Language: {language})",
        'citations': [
            {
                'source': f'NCERT Class {grade} {subject}',
                'page': 42,
                'chapter': 'Sample Chapter',
                'text': 'Sample citation text from NCERT textbook...'
            }
        ],
        'confidence': 0.75,
        'language': language,
        'timestamp': datetime.now().isoformat()
    }

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """
    Handle image upload for OCR processing
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        allowed_extensions = app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'bmp'})
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'Invalid file type'}), 400
        
        filename = str(uuid.uuid4()) + '_' + file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            import pytesseract
            from PIL import Image
            
            tesseract_cmd = app.config.get('TESSERACT_CMD')
            if tesseract_cmd and os.path.exists(tesseract_cmd):
                pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            
            image = Image.open(filepath)
            
            languages = app.config.get('TESSERACT_LANGUAGES', 'eng+hin')
            extracted_text = pytesseract.image_to_string(image, lang=languages)
            
            logger.info(f"OCR completed for {filename}")
            
        except ImportError:
            logger.warning("Pytesseract not available, using placeholder text")
            extracted_text = "Sample extracted text from image. Install Tesseract OCR for actual text extraction."
        except Exception as e:
            logger.error(f"OCR error: {e}")
            extracted_text = "Error extracting text from image."
        
        return jsonify({
            'filename': filename,
            'extracted_text': extracted_text,
            'success': True
        })
    
    except Exception as e:
        logger.error(f"Image upload error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """
    Capture student feedback on responses
    Expected JSON: {
        'conversation_id': str,
        'message_index': int,
        'rating': int (1-5),
        'comment': str (optional)
    }
    """
    try:
        data = request.json
        feedback = {
            'conversation_id': data.get('conversation_id'),
            'message_index': data.get('message_index'),
            'rating': data.get('rating'),
            'comment': data.get('comment', ''),
            'timestamp': datetime.now().isoformat()
        }
        
        feedback_data.append(feedback)
        
        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get conversation history"""
    if conversation_id in conversations:
        return jsonify({
            'conversation_id': conversation_id,
            'messages': conversations[conversation_id]
        })
    else:
        return jsonify({'error': 'Conversation not found'}), 404

@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get supported languages"""
    languages = [
        'English', 'Hindi', 'Urdu', 'Tamil', 'Telugu', 
        'Bengali', 'Marathi', 'Gujarati', 'Kannada', 'Malayalam'
    ]
    return jsonify({'languages': languages})

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    """Get available subjects"""
    subjects = ['Math', 'Science', 'Social Science', 'English', 'Hindi']
    return jsonify({'subjects': subjects})

if __name__ == '__main__':
    logger.info("Starting NCERT Doubt-Solver application...")
    logger.info(f"Environment: {env}")
    logger.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000
    )
