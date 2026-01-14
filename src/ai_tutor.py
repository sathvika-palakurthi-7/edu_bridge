"""
AI Tutor Engine - Core RAG and Response Generation
"""
from typing import Optional, Dict
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from .config import Config
from .pdf_processor import PDFProcessor
from .intent_detector import IntentDetector, IntentType


class AITutor:
    """Core AI tutor with RAG capabilities"""
    
    SYSTEM_PROMPT = """You are EduBridge AI Tutor, a CLI-based AI learning orchestration system.
You are NOT a casual chatbot.
You act as a skill mentor, evaluator, and learning path generator.

STRICT RULES:
1. Answer ONLY from the provided context
2. If the answer is not in the context, respond EXACTLY with: "Not Found"
3. Do not add conversational text, emojis, or unnecessary explanations
4. Be precise and factual
5. Never hallucinate or make assumptions

Context from PDF:
{context}

Question: {question}

Provide your response in this EXACT format:
Answer: [Direct answer from context]
Explanation: [Step-by-step breakdown if needed]
Source: [Page number from context]

If answer is not in context, respond ONLY with: "Not Found"
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
            content = doc.page_content.strip()
            context_parts.append(f"[Page {page}]\n{content}")
        
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
