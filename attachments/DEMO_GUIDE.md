# Demo Guide - NCERT Doubt-Solver UI

## Quick Demo Steps

### 1. Start the Application

**Windows:**
```bash
.\run.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
python app.py
```

Wait for the message:
```
* Running on http://0.0.0.0:5000
```

### 2. Open Browser

Navigate to: **http://localhost:5000**

## UI Feature Walkthrough

### Welcome Screen

On first load, you'll see:
- **Welcome message** with NCERT Doubt-Solver branding
- **4 feature cards** highlighting key capabilities
- **"Start Asking Questions"** button

### Sidebar Configuration

Click the **Settings** button (top-right) to open sidebar:

1. **Grade Selection**: Choose from Class 5-10
2. **Subject Selection**: Math, Science, Social Science, English, Hindi
3. **Language Selection**: 10+ languages including English, Hindi, Urdu, Tamil, Telugu, etc.
4. **New Conversation**: Start fresh chat

### Main Chat Interface

#### Asking Questions

1. **Text Input**:
   - Type your question in the text area
   - Press **Ctrl+Enter** or click **Send** button
   - Watch for typing animation and response

2. **Image Upload**:
   - Click **image icon** 📷 in input area
   - Select image with question
   - OCR will extract text automatically
   - Edit extracted text if needed
   - Send question

3. **Voice Input**:
   - Click **microphone icon** 🎤
   - Allow browser microphone access
   - Speak your question
   - Text appears in input area
   - Send question

### Response Features

Each AI response includes:

1. **Answer Text**: Clear, grade-appropriate explanation
2. **Citations Box**: 
   - Source reference (NCERT textbook)
   - Page number
   - Relevant excerpt
3. **Confidence Score**: Displayed in metadata
4. **Timestamp**: When response was generated

### Message Actions

For each response, you can:
- **📋 Copy**: Copy answer to clipboard
- **⭐ Rate**: Provide feedback (1-5 stars + comment)

### Feedback System

1. Click **Rate** button on any response
2. Select star rating (1-5)
3. Add optional comment
4. Submit feedback
5. See confirmation message

## Demo Scenarios

### Scenario 1: Basic Math Question

```
Grade: 8
Subject: Math
Language: English
Question: "What is the formula for the area of a circle?"
```

**Expected**:
- Clear answer with formula
- Citation from NCERT Class 8 Math
- Confidence score
- Copy and rate options

### Scenario 2: Science Question with Image

```
Grade: 10
Subject: Science
Language: Hindi
Action: Upload diagram of human heart
Question: "इस चित्र में दिखाए गए भागों को समझाइए" (Explain parts shown in this diagram)
```

**Expected**:
- OCR extracts any text from image
- Image appears in chat
- Answer in Hindi
- Citations in Hindi NCERT

### Scenario 3: Multilingual Conversation

```
Grade: 7
Subject: Social Science
Language: Tamil
Question: "பண்டைய இந்தியாவின் வர்த்தக வழிகள் பற்றி கூறுக" (Tell about trade routes of ancient India)
```

**Expected**:
- Response in Tamil
- Citations from Tamil NCERT
- Culturally appropriate examples

### Scenario 4: Out-of-Scope Question

```
Question: "What is quantum computing?"
```

**Expected**:
- "I don't know" response
- Suggestion to ask NCERT-related questions
- No hallucinated answers

### Scenario 5: Conversation Context

```
Question 1: "What is photosynthesis?"
Question 2: "Where does it occur in plants?"
Question 3: "Why is it important?"
```

**Expected**:
- Second and third questions use conversation context
- Coherent multi-turn dialogue
- Maintains topic continuity

## Mobile Testing

### On Phone/Tablet

1. **Find your computer's IP**:
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. **Access from mobile**:
   ```
   http://192.168.x.x:5000
   ```

3. **Test mobile features**:
   - Responsive design
   - Touch-friendly buttons
   - Image upload from camera
   - Voice input
   - Swipe gestures

### PWA Installation

1. Open in Chrome/Edge on mobile
2. Look for "Add to Home Screen" prompt
3. Install as PWA
4. Launch from home screen
5. Enjoy offline capabilities (when implemented)

## API Testing (Advanced)

### Using cURL

**Chat API:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the Pythagorean theorem?",
    "grade": 8,
    "subject": "Math",
    "language": "English"
  }'
```

**Image Upload:**
```bash
curl -X POST http://localhost:5000/api/upload-image \
  -F "image=@path/to/image.jpg"
```

**Feedback:**
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test-123",
    "message_index": 0,
    "rating": 5,
    "comment": "Very helpful!"
  }'
```

### Using Postman

Import the following endpoints:

1. **GET** `/` - Home page
2. **POST** `/api/chat` - Send question
3. **POST** `/api/upload-image` - Upload image
4. **POST** `/api/feedback` - Submit feedback
5. **GET** `/api/languages` - Get supported languages
6. **GET** `/api/subjects` - Get available subjects
7. **GET** `/api/conversation/<id>` - Get conversation history

## Performance Testing

### Latency Test

Measure response time:
```javascript
// In browser console
const start = Date.now();
fetch('/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: "Test question",
    grade: 8,
    subject: "Math",
    language: "English"
  })
})
.then(() => {
  console.log(`Response time: ${Date.now() - start}ms`);
});
```

**Target**: < 3-5 seconds (as per project requirements)

### Load Testing

Use tools like:
- Apache JMeter
- Locust
- Artillery

Example Locust test:
```python
from locust import HttpUser, task

class NCERTUser(HttpUser):
    @task
    def ask_question(self):
        self.client.post("/api/chat", json={
            "message": "What is gravity?",
            "grade": 9,
            "subject": "Science",
            "language": "English"
        })
```

## Browser Compatibility Testing

Test on:
- ✅ Chrome 90+ (Windows, Mac, Android)
- ✅ Firefox 88+ (Windows, Mac, Linux)
- ✅ Safari 14+ (Mac, iOS)
- ✅ Edge 90+ (Windows)

## Accessibility Testing

Test with:
- Screen readers (NVDA, JAWS, VoiceOver)
- Keyboard navigation (Tab, Enter, Esc)
- High contrast mode
- Text scaling (150%, 200%)

## Feature Checklist

### Core Features
- [x] Grade selection (5-10)
- [x] Subject selection
- [x] Multilingual support (10+ languages)
- [x] Text-based questions
- [x] Image upload with OCR
- [x] Voice input
- [x] Conversation history
- [x] Citations display
- [x] Confidence scores
- [x] Feedback system
- [x] Copy answers
- [x] Responsive design
- [x] Mobile-friendly
- [x] PWA support

### Integration Points (To be implemented)
- [ ] OPEA RAG pipeline integration
- [ ] Actual NCERT document retrieval
- [ ] Vector database queries
- [ ] LLM answer generation
- [ ] Fine-tuned regional language models
- [ ] Quality evaluation dataset
- [ ] User authentication
- [ ] Database persistence

## Common Demo Issues

### Issue: "Sample/Placeholder" responses

**Reason**: OPEA RAG pipeline not yet integrated  
**Solution**: This is expected. Focus on UI/UX features

### Issue: OCR returns "Sample text"

**Reason**: Tesseract not installed  
**Solution**: Install Tesseract OCR (see SETUP_GUIDE.md)

### Issue: Voice input not working

**Reason**: Browser doesn't support Web Speech API  
**Solution**: Use Chrome or Edge

### Issue: Mobile layout broken

**Reason**: Cache issue  
**Solution**: Hard refresh (Ctrl+Shift+R)

## Screenshots Guide

For documentation/presentation, capture:

1. **Welcome Screen** - Full desktop view
2. **Chat Interface** - Active conversation
3. **Image Upload** - OCR in action
4. **Citations** - Source references displayed
5. **Feedback Modal** - Rating system
6. **Mobile View** - Responsive design
7. **Sidebar** - Settings panel
8. **Multiple Languages** - Different language demos

## Presentation Tips

When demoing to stakeholders:

1. **Start with Welcome Screen**: Highlight features
2. **Show Grade/Subject Selection**: Emphasize customization
3. **Demo Text Question**: Show basic functionality
4. **Upload Image**: Demonstrate OCR capability
5. **Try Voice Input**: Show accessibility features
6. **Display Citations**: Emphasize accuracy and sources
7. **Submit Feedback**: Show quality improvement loop
8. **Switch Languages**: Demonstrate multilingual support
9. **Show Mobile**: Display responsive design
10. **Explain Integration**: Discuss OPEA pipeline plans

## Metrics to Track

During demo/testing, monitor:

- **Response Time**: Aim for < 5 seconds
- **OCR Accuracy**: Text extraction quality
- **User Satisfaction**: Feedback ratings
- **Error Rate**: Failed requests
- **Conversation Length**: Average turns per session
- **Language Usage**: Which languages are popular
- **Subject Distribution**: Most queried subjects

## Next Demo Phase

Once OPEA pipeline is integrated:

- Real NCERT answers
- Accurate citations
- Context-aware responses
- Multilingual fine-tuned models
- Performance benchmarks
- Quality evaluation results

---

**Ready to Demo!** 🚀

Start the application and explore all features. The UI is production-ready and waiting for the OPEA RAG backend integration.
