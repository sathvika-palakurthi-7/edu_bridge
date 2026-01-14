# EduBridge Installation Guide

## Current Status

Based on verification:
- [OK] Python 3.12.1 installed
- [OK] Ollama is running
- [OK] Project structure complete
- [PENDING] Missing Python dependencies
- [PENDING] Ollama model not pulled

## Step-by-Step Installation

### Step 1: Install Python Dependencies

Open PowerShell in the project directory and run:

```powershell
cd N:\Sathvika\EDUBRIDGE
pip install -r requirements.txt
```

This will install:
- langchain & langchain-community (RAG framework)
- langchain-ollama (Ollama integration)
- chromadb (Vector database)
- pypdf (PDF text extraction)
- sentence-transformers (Embeddings)
- python-dotenv (Environment config)

**Expected time**: 2-5 minutes depending on internet speed

### Step 2: Pull Ollama Model

```powershell
ollama pull llama3.2:1b
```

This downloads the lightweight Llama 3.2 1B model (~1GB).

**Expected time**: 1-3 minutes depending on internet speed

### Step 3: Verify Installation

```powershell
python verify_setup.py
```

You should see all [OK] status:
```
[OK] Python 3.12.1
[OK] langchain - Installed
[OK] langchain_community - Installed
[OK] langchain_ollama - Installed
[OK] chromadb - Installed
[OK] pypdf - Installed
[OK] sentence_transformers - Installed
[OK] dotenv - Installed
[OK] Ollama - Running
[OK] llama3.2:1b - Available
[SUCCESS] All checks passed!
```

### Step 4: Run EduBridge

```powershell
python main.py
```

You should see:
```
╔═══════════════════════════════════════════════════════════╗
║                    EDUBRIDGE AI TUTOR                     ║
║          AI-Powered Skilling & Learning System            ║
╚═══════════════════════════════════════════════════════════╝

Type 'help' for available commands

[OK] Ollama connection successful

EduBridge>
```

### Step 5: Load Your First PDF

```
EduBridge> load "Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf"
```

Expected output:
```
Loading PDF: Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf
Please wait...
Successfully loaded: Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf
Pages processed: [X]
Chunks created: [X]

[SUCCESS] PDF loaded successfully
You can now ask questions about this document
```

### Step 6: Ask Your First Question

```
EduBridge> What is project documentation?
```

Expected format:
```
Processing question...

============================================================
Answer: [Direct answer from PDF]
Explanation: [Step-by-step breakdown]
Source: [Page number]
============================================================
```

## Troubleshooting

### Issue: pip install fails

**Solution 1**: Upgrade pip
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Solution 2**: Install with verbose output
```powershell
pip install -r requirements.txt -v
```

### Issue: Ollama not running

**Check if Ollama is running:**
```powershell
ollama list
```

**If not running, start it:**
```powershell
ollama serve
```

### Issue: Model download fails

**Check Ollama status:**
```powershell
ollama list
```

**Try pulling again:**
```powershell
ollama pull llama3.2:1b
```

### Issue: PDF loading fails

**Common causes:**
1. File path contains spaces - Use quotes: `load "file name.pdf"`
2. File not found - Use full path: `load "N:\Sathvika\EDUBRIDGE\document.pdf"`
3. PDF is scanned image - Only text-based PDFs work
4. PDF is encrypted - Remove password protection first

### Issue: "Not Found" responses

**This is expected when:**
- Question is not covered in the PDF
- Question is too vague
- PDF doesn't contain relevant information

**Try:**
- Rephrasing the question
- Being more specific
- Checking if the topic is in the PDF

## Testing the System

### Test 1: System Commands
```
EduBridge> status
EduBridge> help
```

### Test 2: PDF Loading
```
EduBridge> load "Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf"
```

### Test 3: Conceptual Question
```
EduBridge> What is project documentation?
```

### Test 4: Technical Question
```
EduBridge> How should a fresher explain their project?
```

### Test 5: Out-of-Scope Question
```
EduBridge> What is quantum computing?
```
Expected: `Not Found` (if not in PDF)

## Next Steps

1. Try loading different PDFs
2. Experiment with different question types
3. Test the "Not Found" validation
4. Check the `data/vectorstore` directory for stored embeddings

## Performance Notes

- **First PDF load**: 10-30 seconds (creates embeddings)
- **Subsequent questions**: 2-5 seconds per answer
- **Model**: llama3.2:1b is optimized for speed, not accuracy
- **Accuracy**: Depends on PDF quality and question clarity

## System Requirements

- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: ~2GB for model + dependencies
- **CPU**: Any modern processor (no GPU required)
- **OS**: Windows 10/11

## Support

If you encounter issues:
1. Run `python verify_setup.py` to diagnose
2. Check error messages carefully
3. Verify Ollama is running: `ollama list`
4. Ensure PDF is text-based, not scanned

Happy Learning! 🎓
