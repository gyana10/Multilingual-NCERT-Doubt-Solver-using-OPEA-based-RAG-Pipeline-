# Quick Start - NCERT Doubt-Solver

## 🚀 Get Started in 3 Minutes

### Step 1: Install Tesseract OCR

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**Mac:**
```bash
brew install tesseract
```

### Step 2: Setup Python Environment

```bash
# Navigate to project directory
cd c:\Users\HP\intel

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Run the Application

**Easy Way (Windows):**
```bash
.\run.bat
```

**Manual Way:**
```bash
python app.py
```

### Step 4: Open in Browser

Go to: **http://localhost:5000**

---

## ✨ That's It!

You should now see the NCERT Doubt-Solver welcome screen.

### Quick Tips:

1. **Select Grade**: Choose your class (5-10) from sidebar
2. **Pick Subject**: Math, Science, Social Science, etc.
3. **Choose Language**: English, Hindi, or 8+ other languages
4. **Ask Questions**: Type, upload image, or use voice input

### Need Help?

- **Full Setup Guide**: See `SETUP_GUIDE.md`
- **Demo Guide**: See `DEMO_GUIDE.md`
- **Project Info**: See `README.md`

---

## 📱 Mobile Access

1. Find your computer's IP address
2. On phone, go to: `http://YOUR_IP:5000`
3. Enjoy mobile-optimized experience!

---

## 🔧 Troubleshooting

**Port already in use?**
Change port in `app.py`: `app.run(port=5001)`

**Tesseract not found?**
Update path in `config.py`: `TESSERACT_CMD = r'C:\Your\Path\tesseract.exe'`

**Module errors?**
Reinstall: `pip install -r requirements.txt --force-reinstall`

---

## 🎯 Next Steps

1. ✅ UI is ready to use
2. 🔄 Integrate OPEA RAG pipeline (see `opea_integration.py`)
3. 📚 Ingest NCERT documents
4. 🚀 Deploy to production

**Happy Learning!** 🎓
