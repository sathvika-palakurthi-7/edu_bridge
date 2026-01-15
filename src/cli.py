"""
CLI Interface for EduBridge AI Tutor
"""
import sys
from pathlib import Path
from .ai_tutor import AITutor
from .config import Config


class EduBridgeCLI:
    """Command-line interface for EduBridge"""
    
    BANNER = """
+===========================================================+
|                    EDUBRIDGE AI TUTOR                     |
|          AI-Powered Skilling & Learning System            |
+===========================================================+

Type 'help' for available commands
"""
    
    HELP_TEXT = """
AVAILABLE COMMANDS:
-------------------
load                Load all PDFs from src/syllabus directory
load <pdf_path>     Load a specific PDF document
status              Show current system status
help                Show this help message
exit/quit           Exit the application

ASKING QUESTIONS:
-----------------
Simply type your question after loading PDFs.
The system will analyze the PDF content and provide answers.

RESPONSE FORMAT:
----------------
Answer: [Direct answer from PDF]
Explanation: [Step-by-step breakdown]
Source: [Page number]

If the answer is not found in the PDF, you will see: "Not Found"
"""
    
    def __init__(self):
        self.tutor = AITutor()
        self.running = True
    
    def start(self):
        """Start the CLI application"""
        print(self.BANNER)
        Config.validate()
        
        # Check Ollama connectivity
        self._check_ollama()
        
        while self.running:
            try:
                user_input = input("\nEduBridge> ").strip()
                
                if not user_input:
                    continue
                
                self._process_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\nExiting EduBridge...")
                self.running = False
            except EOFError:
                self.running = False
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def _process_input(self, user_input: str):
        """Process user input"""
        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        
        # System commands
        if command == "help":
            print(self.HELP_TEXT)
        
        elif command in ["exit", "quit"]:
            print("Exiting EduBridge...")
            self.running = False
        
        elif command == "status":
            self._show_status()
        
        elif command == "load":
            if len(parts) < 2:
                # Load all PDFs from src/syllabus directory
                self._load_all_pdfs()
            else:
                # Strip quotes and extra whitespace
                pdf_path = parts[1].strip().strip('"').strip("'")
                self._load_pdf(pdf_path)
        
        else:
            # Treat as question
            self._answer_question(user_input)
    
    def _load_pdf(self, pdf_path: str):
        """Load a PDF document"""
        print(f"\nLoading PDF: {pdf_path}")
        print("Please wait...")
        
        success = self.tutor.load_pdf(pdf_path)
        
        if success:
            print("\n[SUCCESS] PDF loaded successfully")
            print("You can now ask questions about this document")
        else:
            print("\n[FAILED] Failed to load PDF")
    
    def _load_all_pdfs(self):
        """Load all PDFs from src/syllabus directory"""
        print("\nLoading all PDFs from src/syllabus directory...")
        print("Please wait...")
        
        success, count = self.tutor.load_all_pdfs()
        
        if success:
            print(f"\n[SUCCESS] Successfully loaded all {count} PDF(s) from src/syllabus")
            print("You can now ask questions from these documents")
        else:
            print("\n[FAILED] Failed to load PDFs from src/syllabus directory")
    
    def _answer_question(self, question: str):
        """Answer a user question"""
        print("\nProcessing question...")
        
        response = self.tutor.answer_question(question)
        
        print("\n" + "="*60)
        print(response)
        print("="*60)
    
    def _show_status(self):
        """Show system status"""
        status = self.tutor.get_status()
        
        print("\nSYSTEM STATUS:")
        print("-" * 40)
        for key, value in status.items():
            print(f"{key:15}: {value}")
        print("-" * 40)
    
    def _check_ollama(self):
        """Check if Ollama is running"""
        try:
            import requests
            response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=2)
            if response.status_code == 200:
                print("[OK] Ollama connection successful")
            else:
                print("[WARNING] Ollama may not be running properly")
        except Exception:
            print("[WARNING] Cannot connect to Ollama")
            print(f"  Make sure Ollama is running at {Config.OLLAMA_BASE_URL}")
            print(f"  Model required: {Config.OLLAMA_MODEL}")


def main():
    """Entry point for CLI application"""
    cli = EduBridgeCLI()
    cli.start()


if __name__ == "__main__":
    main()
