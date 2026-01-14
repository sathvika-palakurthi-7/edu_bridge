# EduBridge System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER (CLI)                              │
│                    python main.py                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CLI Interface                              │
│                      (src/cli.py)                               │
│                                                                 │
│  Commands: load, status, help, exit                            │
│  Input Processing & Output Formatting                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Intent Detector                              │
│                (src/intent_detector.py)                         │
│                                                                 │
│  ┌──────────┬──────────┬──────────┬──────────┐                │
│  │Conceptual│Technical │PDF-Based │  System  │                │
│  └──────────┴──────────┴──────────┴──────────┘                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI Tutor Engine                            │
│                    (src/ai_tutor.py)                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐       │
│  │  RAG Pipeline                                       │       │
│  │  1. Retrieve context from vector store              │       │
│  │  2. Augment prompt with context                     │       │
│  │  3. Generate response via Ollama                    │       │
│  │  4. Validate & format output                        │       │
│  └─────────────────────────────────────────────────────┘       │
└────────────┬────────────────────────────┬───────────────────────┘
             │                            │
             ▼                            ▼
┌────────────────────────┐   ┌───────────────────────────────────┐
│   PDF Processor        │   │      Ollama LLM                   │
│ (src/pdf_processor.py) │   │   (llama3.2:1b)                   │
│                        │   │                                   │
│  ┌──────────────────┐  │   │  Local AI Inference               │
│  │ PyPDF Extraction │  │   │  Temperature: 0.1                 │
│  └──────────────────┘  │   │  Context-aware generation         │
│           ▼            │   └───────────────────────────────────┘
│  ┌──────────────────┐  │
│  │ Text Chunking    │  │
│  │ (1000/200)       │  │
│  └──────────────────┘  │
│           ▼            │
│  ┌──────────────────┐  │
│  │ HuggingFace      │  │
│  │ Embeddings       │  │
│  │ (MiniLM-L6-v2)   │  │
│  └──────────────────┘  │
│           ▼            │
│  ┌──────────────────┐  │
│  │ ChromaDB         │  │
│  │ Vector Store     │  │
│  └──────────────────┘  │
└────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────┐
│  User Input │
│  "Question" │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Intent Detection    │
│ Classify question   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐      ┌──────────────────┐
│ Check PDF Loaded?   │──NO──▶│ Return Error     │
└──────┬──────────────┘      └──────────────────┘
       │ YES
       ▼
┌─────────────────────┐
│ Vector Search       │
│ Query embeddings    │
│ Retrieve top-k docs │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Build Context       │
│ Combine chunks      │
│ Add metadata        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Create Prompt       │
│ System + Context    │
│ + Question          │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Ollama LLM          │
│ Generate response   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐      ┌──────────────────┐
│ Validate Response   │──NO──▶│ Return           │
│ Check if found      │      │ "Not Found"      │
└──────┬──────────────┘      └──────────────────┘
       │ YES
       ▼
┌─────────────────────┐
│ Format Output       │
│ Answer/Explanation/ │
│ Source              │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Display to User     │
└─────────────────────┘
```

## Component Interaction

```
┌──────────────┐
│   main.py    │  Entry point
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────────────┐
│                      CLI Module                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │ start()    │  │ process()  │  │ display()  │        │
│  └────────────┘  └────────────┘  └────────────┘        │
└──────┬───────────────────┬───────────────┬──────────────┘
       │                   │               │
       ▼                   ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Config       │  │ Intent       │  │ AI Tutor     │
│ Management   │  │ Detector     │  │ Engine       │
└──────────────┘  └──────────────┘  └──────┬───────┘
                                            │
                          ┌─────────────────┴─────────────────┐
                          │                                   │
                          ▼                                   ▼
                  ┌──────────────┐                  ┌──────────────┐
                  │ PDF          │                  │ Ollama       │
                  │ Processor    │                  │ LLM          │
                  └──────┬───────┘                  └──────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ ChromaDB     │
                  │ Vector Store │
                  └──────────────┘
```

## File Dependencies

```
main.py
  └── src/cli.py
       ├── src/config.py
       ├── src/ai_tutor.py
       │    ├── src/config.py
       │    ├── src/pdf_processor.py
       │    │    ├── src/config.py
       │    │    ├── pypdf (external)
       │    │    ├── langchain (external)
       │    │    ├── chromadb (external)
       │    │    └── sentence_transformers (external)
       │    ├── src/intent_detector.py
       │    └── langchain_ollama (external)
       └── requests (external)
```

## RAG Pipeline Detail

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG PIPELINE                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. RETRIEVAL                                               │
│     ┌──────────────────────────────────────┐               │
│     │ User Question                        │               │
│     │   ↓                                  │               │
│     │ Embed Question (HuggingFace)         │               │
│     │   ↓                                  │               │
│     │ Semantic Search (ChromaDB)           │               │
│     │   ↓                                  │               │
│     │ Top-K Relevant Chunks (k=3)          │               │
│     └──────────────────────────────────────┘               │
│                                                             │
│  2. AUGMENTATION                                            │
│     ┌──────────────────────────────────────┐               │
│     │ System Prompt (Rules)                │               │
│     │   +                                  │               │
│     │ Retrieved Context (Chunks)           │               │
│     │   +                                  │               │
│     │ User Question                        │               │
│     │   ↓                                  │               │
│     │ Complete Prompt                      │               │
│     └──────────────────────────────────────┘               │
│                                                             │
│  3. GENERATION                                              │
│     ┌──────────────────────────────────────┐               │
│     │ Send to Ollama (llama3.2:1b)         │               │
│     │   ↓                                  │               │
│     │ LLM Processing                       │               │
│     │   ↓                                  │               │
│     │ Generated Response                   │               │
│     └──────────────────────────────────────┘               │
│                                                             │
│  4. VALIDATION                                              │
│     ┌──────────────────────────────────────┐               │
│     │ Check if answer found                │               │
│     │   ↓                                  │               │
│     │ YES: Format as Answer/Explanation/   │               │
│     │      Source                          │               │
│     │   ↓                                  │               │
│     │ NO: Return "Not Found"               │               │
│     └──────────────────────────────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Storage Structure

```
EDUBRIDGE/
├── data/
│   └── vectorstore/          # ChromaDB storage
│       ├── chroma.sqlite3    # Vector database
│       └── [embeddings]      # Stored embeddings
│
├── src/                      # Source code
│   ├── __pycache__/          # Python cache
│   └── *.py                  # Python modules
│
└── [project files]           # Config, docs, etc.
```

## Configuration Flow

```
┌──────────────┐
│ .env file    │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────┐
│ src/config.py                        │
│                                      │
│ Config.OLLAMA_BASE_URL               │
│ Config.OLLAMA_MODEL                  │
│ Config.VECTOR_STORE_PATH             │
│ Config.CHUNK_SIZE                    │
│ Config.CHUNK_OVERLAP                 │
└──────┬───────────────────────────────┘
       │
       ├──────────────────┬──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ AI Tutor     │  │ PDF          │  │ CLI          │
│ (LLM config) │  │ Processor    │  │ (Display)    │
│              │  │ (Chunking)   │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Error Handling Flow

```
┌─────────────────┐
│ User Action     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Try: Execute            │
└────────┬────────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐  ┌──────────────────┐
│Success │  │ Exception        │
└────────┘  └────────┬─────────┘
                     │
              ┌──────┴──────┬──────────────┬────────────┐
              │             │              │            │
              ▼             ▼              ▼            ▼
        ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐
        │PDF Load │  │Ollama    │  │Vector    │  │General  │
        │Error    │  │Error     │  │Store     │  │Error    │
        └────┬────┘  └────┬─────┘  └────┬─────┘  └────┬────┘
             │            │             │             │
             └────────────┴─────────────┴─────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │ Display Error    │
                │ Continue/Exit    │
                └──────────────────┘
```

## Security & Privacy Model

```
┌─────────────────────────────────────────────────────────┐
│                  LOCAL EXECUTION                        │
│                                                         │
│  ┌─────────────┐      ┌─────────────┐                 │
│  │   User PC   │      │   Ollama    │                 │
│  │             │◄────▶│   (Local)   │                 │
│  └─────────────┘      └─────────────┘                 │
│         │                                              │
│         ▼                                              │
│  ┌─────────────┐                                       │
│  │  ChromaDB   │                                       │
│  │  (Local)    │                                       │
│  └─────────────┘                                       │
│                                                         │
│  NO INTERNET REQUIRED                                  │
│  NO DATA SENT TO CLOUD                                 │
│  COMPLETE PRIVACY                                      │
└─────────────────────────────────────────────────────────┘
```

---

**Legend:**
- `┌─┐` : Component/Module
- `│ │` : Boundary
- `▼ ▲` : Data flow direction
- `◄─►` : Bidirectional communication
- `├─┤` : Connection point
