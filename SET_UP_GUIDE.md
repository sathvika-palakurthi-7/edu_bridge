# EDUBRIDGE Setup Guide

Complete setup instructions for new users after cloning the repository.

---

## 📋 Prerequisites

Before you begin, ensure you have:
- **Python 3.8+** installed
- **Git** installed
- **Internet connection** (for initial setup)
- **4GB+ RAM** recommended

---

## 🚀 Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/sathvika-palakurthi-7/edu_bridge.git
cd edu_bridge
```

### 2. Install Ollama (CRITICAL - App won't work without this!)

**For Windows:**
1. Download from: https://ollama.ai
2. Run the installer
3. Verify installation:
   ```bash
   ollama --version
   ```

**For Linux/macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 3. Start Ollama Service

**Open a separate terminal and run:**
```bash
ollama serve
```

> ⚠️ **IMPORTANT**: Keep this terminal running while using EDUBRIDGE!

### 4. Pull the Required LLM Model

**In another terminal:**
```bash
ollama pull llama3.2:1b
```

Wait for the download to complete (~1GB). Verify:
```bash
ollama list
```

You should see `llama3.2:1b` in the list.

### 5. Install Tesseract-OCR (Optional - for scanned PDFs)

**For Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer (default path: `C:\Program Files\Tesseract-OCR`)
3. Verify:
   ```bash
   tesseract --version
   ```

**For Linux:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

**For macOS:**
```bash
brew install tesseract
```

> 📝 **Note**: If you skip this, text-based PDFs will still work but scanned/image PDFs won't.

### 6. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# For Windows:
venv\Scripts\activate

# For Linux/macOS:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 7. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 8. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages (~2-5 minutes).

### 9. Configure Environment Variables

```bash
# Copy the example environment file
# For Windows:
copy .env.example .env

# For Linux/macOS:
cp .env.example .env
```

**Optional**: Edit `.env` if you need custom settings:
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b
VECTOR_STORE_PATH=./data/vectorstore
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 10. Verify Installation

**Run the verification script:**
```bash
python verify_setup.py
```

This checks:
- ✅ Python version
- ✅ All dependencies installed
- ✅ Ollama connectivity
- ✅ llama3.2:1b model available
- ✅ Tesseract-OCR (if installed)
- ✅ Project structure

**Expected output:**
```
[OK] Python 3.x.x
[OK] Ollama - Running
[OK] llama3.2:1b - Available
[SUCCESS] All checks passed!
```

### 11. Run the Application

```bash
python main.py
```

You should see:
```
+===========================================================+
|                    EDUBRIDGE AI TUTOR                     |
|          AI-Powered Skilling & Learning System            |
+===========================================================+

[OK] Ollama connection successful

EduBridge>
```

---

## 📚 Quick Start Usage

### Load PDFs and Ask Questions

```
EduBridge> load
Found 2 PDF(s) in syllabus directory
[SUCCESS] Successfully loaded all 2 PDF(s)

EduBridge> What is prompt engineering?

Processing question...
============================================================
Answer: [Your answer will appear here]
============================================================
```

### Available Commands

| Command | Description |
|---------|-------------|
| `load` | Load all PDFs from src/syllabus |
| `load <path>` | Load a specific PDF |
| `status` | Show system status |
| `help` | Show help message |
| `exit` or `quit` | Exit application |

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to Ollama"

**Solution:**
```bash
# In a separate terminal, run:
ollama serve
```

### Issue: "Model 'llama3.2:1b' not found"

**Solution:**
```bash
ollama pull llama3.2:1b
```

### Issue: "ModuleNotFoundError"

**Solution:**
```bash
# Make sure virtual environment is activated
# Then reinstall:
pip install -r requirements.txt
```

### Issue: "PDF loading failed - scanned document"

**Solution:**
Install Tesseract-OCR (see Step 5)

### Issue: Import errors or package conflicts

**Solution:**
```bash
# Deactivate and remove old venv
deactivate
rm -rf venv  # or rmdir /s venv on Windows

# Recreate from scratch
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔧 System Requirements

### Minimum:
- Python 3.8+
- 4GB RAM
- 2GB free disk space
- Internet (initial setup only)

### Recommended:
- Python 3.10+
- 8GB RAM
- SSD storage
- GPU (optional, for faster inference)

---

## 📞 Support

If you encounter issues:

1. **Check documentation:**
   - `README.md` - Full documentation
   - `QUICKSTART.md` - Quick start guide
   - `TESTING_GUIDE.md` - Testing instructions
   - `ANALYSIS.md` - System analysis and improvements

2. **Run verification:**
   ```bash
   python verify_setup.py
   ```

3. **Check logs:**
   - Look for error messages in terminal output

---

## ✅ Final Checklist

Before running the application, ensure:

- [ ] Ollama is installed and running (`ollama serve`)
- [ ] Model is downloaded (`ollama list` shows llama3.2:1b)
- [ ] Virtual environment is activated (see `(venv)` in prompt)
- [ ] Dependencies are installed (`pip list` shows all packages)
- [ ] `.env` file exists (copied from `.env.example`)
- [ ] Verification script passes (`python verify_setup.py`)
- [ ] Tesseract-OCR installed (optional, for scanned PDFs)

**When all checked, you're ready to run:**
```bash
python main.py
```

---

**Happy Learning! 🎓**

*Built with ❤️ for Engineering Students*
