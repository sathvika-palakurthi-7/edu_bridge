# EduBridge AI Tutor

**AI-Powered Skilling & Learning Backend for Engineering Students**

EduBridge is a CLI-based AI tutor that uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware answers from PDF documents using locally installed Ollama models.

## Features

✅ **PDF-Based Learning**: Load any PDF and ask questions about its content  
✅ **RAG Architecture**: Uses vector embeddings and semantic search for accurate retrieval  
✅ **Local AI**: Powered by Ollama (llama3.2:1b) - runs completely offline  
✅ **Strict Validation**: No hallucinations - answers only from provided context  
✅ **Intent Detection**: Automatically categorizes questions (conceptual/technical/PDF-based)  
✅ **Structured Output**: Answer/Explanation/Source format for clarity  
✅ **Robust PDF Processing**: PyMuPDF with automatic document repair  
✅ **OCR Support**: Tesseract-OCR fallback for scanned/image-based PDFs  
✅ **Smart Error Handling**: Graceful degradation and helpful error messages

## Tech Stack

- **Python 3.12+**
- **LangChain**: RAG orchestration (v1.2.0+)
- **Ollama**: Local LLM inference (llama3.2:1b)
- **ChromaDB**: Vector store for embeddings
- **HuggingFace**: Sentence transformers for embeddings
- **PyMuPDF (fitz)**: Advanced PDF text extraction with repair capabilities
- **Tesseract-OCR**: Optical character recognition for scanned PDFs
- **Pillow**: Image processing for OCR pipeline

## Prerequisites

### 1. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai)

### 2. Pull the Model

```bash
ollama pull llama3.2:1b
```

### 3. Start Ollama Service

**Important**: Ollama must be running before starting EduBridge.

```bash
ollama serve
```

Keep this terminal open while using EduBridge.

### 4. Install Tesseract-OCR (Optional - for scanned PDFs)

**For Windows:**

1. Download from: [Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer (default path: `C:\Program Files\Tesseract-OCR`)
3. Add to System PATH (optional - EduBridge auto-detects default installation)
4. Restart your terminal

**Verify Installation:**

```bash
tesseract --version
```

**Note**: If Tesseract is not installed, EduBridge will still work for text-based PDFs but cannot process scanned/image PDFs.

### 5. Verify Setup

```bash
ollama list
python verify_setup.py
```

## Installation

### 1. Clone/Navigate to Project

```bash
cd N:\Sathvika\EDUBRIDGE
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:

- `pytesseract` and `Pillow` (OCR support)
- `pymupdf` (robust PDF processing)
- `langchain` and related packages (RAG framework)
- `chromadb` (vector database)
- `sentence-transformers` (embeddings)
- `python-dotenv` (configuration)

### 4. Configure Environment

```bash
copy .env.example .env
```

Edit `.env` if needed (default settings work for most cases)

## Usage

### Start the Application

```bash
python main.py
```

### Available Commands

| Command           | Description                      |
| ----------------- | -------------------------------- |
| `load <pdf_path>` | Load a PDF document for tutoring |
| `status`          | Show current system status       |
| `help`            | Show available commands          |
| `exit` or `quit`  | Exit the application             |

### Example Session

```
EduBridge> load "Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf"

Loading PDF: Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf
Please wait...
Successfully loaded: Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf
Pages processed: 15
Chunks created: 42

✓ PDF loaded successfully
You can now ask questions about this document

EduBridge> What is project documentation?

Processing question...

============================================================
Answer: Project documentation is a comprehensive collection of documents that describe the project's objectives, scope, deliverables, timelines, and processes.

Explanation: Project documentation serves as a reference guide for all stakeholders involved in the project. It includes requirements specifications, design documents, test plans, and user manuals that help ensure everyone understands the project goals and implementation details.

Source: Page 3
============================================================

EduBridge> How should a fresher explain their project?

Processing question...

============================================================
Answer: A fresher should explain their project by focusing on the problem statement, their role, technologies used, implementation approach, and key learnings.

Explanation: Start with the business problem the project solves, then describe your specific contributions, the tech stack you worked with, challenges faced, and how you overcame them. Conclude with measurable outcomes and what you learned from the experience.

Source: Page 7
============================================================

EduBridge> status

SYSTEM STATUS:
----------------------------------------
PDF Loaded     : Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf
Model          : llama3.2:1b
Ollama URL     : http://localhost:11434
Status         : Ready
----------------------------------------

EduBridge> exit
Exiting EduBridge...
```

## Response Format

All answers follow this strict format:

```
Answer: [Direct answer extracted from PDF context]
Explanation: [Step-by-step breakdown if applicable]
Source: [Page number from PDF]
```

If the answer cannot be found in the PDF:

```
Not Found
```

## Architecture

```
┌─────────────────┐
│   CLI Input     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Intent Detector │ ──► Categorize: Conceptual/Technical/PDF-based/System
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PDF Processor   │ ──► Extract text → Chunk → Embed → Store in ChromaDB
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vector Search   │ ──► Retrieve top-k relevant chunks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Ollama LLM      │ ──► Generate answer from context only
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Response Format │ ──► Answer/Explanation/Source or "Not Found"
└─────────────────┘
```

## Configuration

Edit `.env` to customize:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b

# Vector Store Configuration
VECTOR_STORE_PATH=./data/vectorstore
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

## Design Principles

1. **No Hallucinations**: Answers only from provided PDF context
2. **Strict Validation**: "Not Found" response when answer is uncertain
3. **Context-Restricted**: AI cannot make assumptions beyond the document
4. **Source Attribution**: Every answer includes page reference
5. **Skill-Focused**: Designed for engineering students' learning needs

## Troubleshooting

### Ollama Connection Error

```
Error generating response: [WinError 10061] No connection could be made because the target machine actively refused it
```

**Solution**: Ollama is not running. Start it in a separate terminal:

```bash
ollama serve
```

Keep this terminal open and try your question again in EduBridge.

### Model Not Found

```
Error: model 'llama3.2:1b' not found
```

**Solution**: Pull the model:

```bash
ollama pull llama3.2:1b
```

### PDF Loading Failed - Scanned Document

```
[IMPORTANT] This PDF appears to be a scanned image.
To extract text, please install Tesseract-OCR on your system
```

**Solution**:

1. Install Tesseract-OCR from [Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki)
2. Restart your terminal
3. Run `python verify_setup.py` to confirm OCR is detected
4. Try loading the PDF again

### PDF Loading Failed - Corrupted/Malformed PDF

```
Error: No text content found in PDF after repair attempt
```

**Solutions**:

- **For corrupted PDFs**: PyMuPDF automatically attempts repair. If it still fails, the PDF may be severely damaged.
- **For scanned PDFs**: Install Tesseract-OCR (see above)
- **For encrypted PDFs**: Remove password protection first
- **For image-only PDFs**: Install Tesseract-OCR for OCR processing

### Path Issues with Quoted Filenames

If you get "File not found" errors:

- Use quotes for paths with spaces: `load "my file.pdf"`
- Or use paths without spaces: `load my_file.pdf`
- Use relative paths: `load src/syllabus/document.pdf"`
- Or absolute paths: `load "N:\Sathvika\EDUBRIDGE\file.pdf"`

### Import Errors (ModuleNotFoundError)

```
ModuleNotFoundError: No module named 'langchain.prompts'
```

**Solution**: The LangChain package structure changed. This is already fixed in the code, but if you see this:

```bash
pip install --upgrade langchain langchain-core langchain-community langchain-ollama
```

### OCR Not Detected (Tesseract Installed)

```
Page X: No text found and OCR (Tesseract) is not installed.
```

**Solution**: EduBridge auto-detects Tesseract at `C:\Program Files\Tesseract-OCR\tesseract.exe`. If installed elsewhere:

1. Verify installation: `tesseract --version`
2. Run verification: `python verify_setup.py`
3. Check the OCR section shows `[OK]`

### Verification Script

Run the comprehensive setup verification:

```bash
python verify_setup.py
```

This checks:

- Python version
- All dependencies
- Ollama connectivity
- Ollama model availability
- OCR support (Tesseract)
- Project file structure

## Project Structure

```
EDUBRIDGE/
├── src/
│   ├── __init__.py
│   ├── cli.py              # CLI interface
│   ├── ai_tutor.py         # Core RAG engine with Ollama
│   ├── pdf_processor.py    # PDF loading, OCR & vector store (PyMuPDF)
│   ├── intent_detector.py  # Question classification
│   ├── config.py           # Configuration management
│   └── syllabus/           # Example: Store your PDF documents here
│       └── AI_Agents_1761113188.pdf
├── data/
│   └── vectorstore/        # ChromaDB storage (auto-created)
├── main.py                 # Entry point
├── verify_setup.py         # Setup verification script
├── debug_pdf_load.py       # PDF loading debug utility
├── pull_model.py           # Ollama model pull utility
├── requirements.txt        # Dependencies
├── .env                    # Environment configuration
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Future Enhancements

### Completed ✅

- [x] OCR support for scanned PDFs (Tesseract integration)
- [x] Robust PDF processing with PyMuPDF
- [x] Automatic document repair for corrupted PDFs

### Planned 📋

- [ ] Multi-PDF support with source tracking
- [ ] Skill gap analysis from PDF content
- [ ] Learning path generation
- [ ] Progress tracking and history
- [ ] Mock interview mode
- [ ] Quiz generation from PDF content
- [ ] Conversation history export
- [ ] Support for other document formats (DOCX, TXT, Markdown)
- [ ] Advanced OCR with language detection
- [ ] Batch PDF processing

## License

MIT License - Built for educational purposes

## Author

EduBridge Team - AI-Powered Skilling Platform
