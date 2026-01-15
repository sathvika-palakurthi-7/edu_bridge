"""
AI Tutor Engine - Core RAG and Response Generation
"""
from typing import Optional, Dict, Tuple
from pathlib import Path
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from .config import Config
from .pdf_processor import PDFProcessor
from .intent_detector import IntentDetector, IntentType


class AITutor:
    """Core AI tutor with RAG capabilities"""
    
    SYSTEM_PROMPT = """You are EduBridge AI Tutor - a friendly, helpful mentor who explains things clearly and concisely.

TEACHING STYLE:
1. Be warm and conversational, but GET TO THE POINT quickly
2. Keep answers SHORT - 2-3 sentences maximum for the Answer section
3. Use simple, everyday language - no unnecessary fluff
4. Break down complex ideas into bite-sized pieces
5. Be encouraging but brief

CRITICAL RULES:
1. Base your answers ONLY on the provided context from the PDFs
2. If the answer is not in the context, respond EXACTLY with: "Not Found"
3. Never make up facts - stay truthful to the PDF content
4. Keep it SHORT and SIMPLE - students want quick, clear answers

Context from the study materials:
{context}

Student's Question: {question}

Respond in this format (keep it concise!):

Answer: [1-3 sentences max - clear and friendly explanation]

Explanation: [2-4 sentences - break it down simply, explain why it matters]

Source: [PDF name, Page number - e.g., "22-promptengg.pdf, Page 5"]

Remember: Be friendly but BRIEF. Quality over quantity!
"""
    
    def __init__(self):
        self.llm = OllamaLLM(
            base_url=Config.OLLAMA_BASE_URL,
            model=Config.OLLAMA_MODEL,
            temperature=Config.TEMPERATURE
        )
        self.pdf_processor = PDFProcessor()
        self.intent_detector = IntentDetector()
        self.prompt_template = PromptTemplate(
            template=self.SYSTEM_PROMPT,
            input_variables=["context", "question"]
        )
    
    def load_pdf(self, pdf_path: str) -> bool:
        """Load a PDF for tutoring"""
        return self.pdf_processor.load_pdf(pdf_path)
    
    def load_all_pdfs(self) -> Tuple[bool, int]:
        """
        Load all PDFs from src/syllabus directory
        
        Returns:
            Tuple of (success: bool, count: int)
        """
        # Get the src/syllabus directory relative to this file
        current_dir = Path(__file__).parent
        syllabus_dir = current_dir / "syllabus"
        
        if not syllabus_dir.exists():
            print(f"Error: Directory not found: {syllabus_dir}")
            return False, 0
        
        # Find all PDF files in the directory
        pdf_files = list(syllabus_dir.glob("*.pdf"))
        
        if not pdf_files:
            print(f"Error: No PDF files found in {syllabus_dir}")
            return False, 0
        
        print(f"Found {len(pdf_files)} PDF(s) in syllabus directory")
        
        # Load all PDFs
        success = self.pdf_processor.load_multiple_pdfs(pdf_files)
        
        if success:
            return True, len(pdf_files)
        else:
            return False, 0
    
    def answer_question(self, question: str) -> str:
        """
        Answer a question using RAG
        
        Args:
            question: User's question
            
        Returns:
            Formatted answer or "Not Found"
        """
        # Check if PDF is loaded
        if not self.pdf_processor.is_loaded():
            return "Need to validate: No PDF loaded. Use 'load <pdf_path>' command first."
        
        # Detect intent
        intent, processed_query = self.intent_detector.detect(question)
        
        # Search for relevant context
        relevant_docs = self.pdf_processor.search(processed_query)
        
        if not relevant_docs:
            return "Not Found"
        
        # Build context from retrieved documents
        context_parts = []
        for doc in relevant_docs:
            page = doc.metadata.get('page', 'Unknown')
            source = doc.metadata.get('source', 'Unknown PDF')
            content = doc.page_content.strip()
            context_parts.append(f"[Source: {source}, Page {page}]\n{content}")
        
        context = "\n\n".join(context_parts)
        
        # Generate response
        try:
            prompt = self.prompt_template.format(
                context=context,
                question=processed_query
            )
            
            response = self.llm.invoke(prompt)
            
            # Validate response
            if not response or response.strip().lower() in ["not found", "unknown", ""]:
                return "Not Found"
            
            return response.strip()
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def get_status(self) -> Dict[str, str]:
        """Get current system status"""
        return {
            "PDF Loaded": self.pdf_processor.get_current_pdf(),
            "Model": Config.OLLAMA_MODEL,
            "Ollama URL": Config.OLLAMA_BASE_URL,
            "Status": "Ready" if self.pdf_processor.is_loaded() else "No PDF loaded"
        }
