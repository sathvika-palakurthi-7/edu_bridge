"""
PDF Processing and Vector Store Management
"""
import os
import sys
import logging
from pathlib import Path
from typing import List
from PIL import Image
import pytesseract

# Suppress pymupdf warnings if needed (modern versions use different methods)
import fitz

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from .config import Config


class PDFProcessor:
    """Handles PDF loading, chunking, and vector store creation using PyMuPDF and OCR fallback"""
    
    def __init__(self):
        # Point to default Tesseract installation path on Windows
        self._set_tesseract_path()
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        self.vectorstore = None
        self.current_pdf = None
        self._tesseract_available = self._check_tesseract()
    
    def _set_tesseract_path(self):
        """Set Tesseract path explicitly for Windows if not in PATH"""
        default_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        if os.name == 'nt' and os.path.exists(default_path):
            pytesseract.pytesseract.tesseract_cmd = default_path

    def _check_tesseract(self) -> bool:
        """Check if Tesseract-OCR is installed and accessible"""
        try:
            # Try to get version to verify it works
            pytesseract.get_tesseract_version()
            return True
        except Exception:
            return False

    def load_pdf(self, pdf_path: str) -> bool:
        """
        Load PDF using PyMuPDF (fitz) with OCR fallback for scanned content.
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            pdf_path = Path(pdf_path)
            if not pdf_path.exists():
                print(f"Error: PDF file not found at {pdf_path}")
                return False
            
            if not pdf_path.suffix.lower() == '.pdf':
                print(f"Error: File must be a PDF")
                return False

            print(f"Analyzing PDF: {pdf_path.name}...")
            
            documents = []
            try:
                # fitz.open handles internal repair automatically
                doc = fitz.open(str(pdf_path))
                
                if doc.is_closed or doc.page_count == 0:
                    raise Exception("PDF document is empty or could not be opened.")

                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    
                    # 1. Try standard text extraction
                    text = page.get_text("text").strip()
                    
                    # 2. Fall back to OCR if no text found and Tesseract is available
                    if not text:
                        if self._tesseract_available:
                            print(f"Page {page_num + 1}: No text found, attempting OCR...")
                            # Render page to image
                            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # Higher resolution for better OCR
                            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                            text = pytesseract.image_to_string(img).strip()
                        else:
                            print(f"Page {page_num + 1}: No text found and OCR (Tesseract) is not installed.")
                    
                    if text:
                        documents.append(
                            Document(
                                page_content=text,
                                metadata={
                                    "source": pdf_path.name,
                                    "page": page_num + 1
                                }
                            )
                        )
                doc.close()
                
            except Exception as e:
                print(f"Error during PDF processing: {str(e)}")
                return False

            if not documents:
                if not self._tesseract_available:
                    print("\n[IMPORTANT] This PDF appears to be a scanned image.")
                    print("To extract text, please install Tesseract-OCR on your system:")
                    print("1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
                    print("2. Add it to your System PATH")
                    print("3. Restart your terminal")
                else:
                    print("Error: No text content could be extracted even after OCR attempt.")
                return False
            
            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            if not chunks:
                print("Error: Failed to create text chunks from PDF content.")
                return False

            # Create vector store
            print(f"Creating knowledge base for {pdf_path.name}...")
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=Config.VECTOR_STORE_PATH
            )
            
            self.current_pdf = pdf_path.name
            print(f"Successfully loaded: {pdf_path.name}")
            print(f"Pages processed: {len(documents)}")
            print(f"Chunks created: {len(chunks)}")
            
            return True
            
        except Exception as e:
            print(f"Fatal error loading PDF: {str(e)}")
            return False
    
    def search(self, query: str, k: int = None) -> List[Document]:
        """
        Search vector store for relevant documents
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if not self.vectorstore:
            return []
        
        k = k or Config.MAX_CONTEXT_DOCS
        return self.vectorstore.similarity_search(query, k=k)
    
    def is_loaded(self) -> bool:
        """Check if a PDF is currently loaded"""
        return self.vectorstore is not None
    
    def get_current_pdf(self) -> str:
        """Get name of currently loaded PDF"""
        return self.current_pdf or "None"
