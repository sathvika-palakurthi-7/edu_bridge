# EduBridge AI Tutor - Quick Start Guide

## Step 1: Install Ollama

1. Download Ollama from: https://ollama.ai
2. Install and run Ollama
3. Pull the model:
   ```bash
   ollama pull llama3.2:1b
   ```

## Step 2: Setup Python Environment

```bash
# Navigate to project directory
cd N:\Sathvika\EDUBRIDGE

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Run EduBridge

```bash
python main.py
```

## Step 4: Load Your PDF

```
EduBridge> load "Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf"
```

## Step 5: Ask Questions

```
EduBridge> What is project documentation?
EduBridge> How should a fresher explain their project?
EduBridge> What are the key components of a project?
```

## Common Commands

- `status` - Check system status
- `help` - Show available commands
- `exit` - Quit application

## Troubleshooting

### If Ollama is not running:
```bash
ollama serve
```

### If model is missing:
```bash
ollama pull llama3.2:1b
```

### If dependencies fail to install:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Expected Behavior

✅ **Found in PDF**: Returns Answer/Explanation/Source format  
❌ **Not in PDF**: Returns exactly "Not Found"  
⚠️ **No PDF loaded**: Returns "Need to validate: No PDF loaded..."

## Example Session

```
╔═══════════════════════════════════════════════════════════╗
║                    EDUBRIDGE AI TUTOR                     ║
║          AI-Powered Skilling & Learning System            ║
╚═══════════════════════════════════════════════════════════╝

Type 'help' for available commands

✓ Ollama connection successful

EduBridge> load "Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf"

Loading PDF: Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf
Please wait...
Successfully loaded: Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf
Pages processed: 15
Chunks created: 42

✓ PDF loaded successfully
You can now ask questions about this document

EduBridge> What is the purpose of project documentation?

Processing question...

============================================================
Answer: Project documentation serves as a comprehensive record of the project's objectives, processes, and outcomes.

Explanation: It helps stakeholders understand the project scope, technical implementation, and business value. For freshers, it demonstrates their ability to communicate technical concepts clearly and professionally.

Source: Page 2
============================================================

EduBridge> exit
Exiting EduBridge...
```

## Next Steps

1. Try loading different PDFs
2. Ask conceptual and technical questions
3. Test the "Not Found" response with questions outside PDF scope
4. Check the `data/vectorstore` directory to see stored embeddings

Happy Learning! 🎓
