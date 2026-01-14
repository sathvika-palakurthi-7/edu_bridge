"""
Intent Detection and Question Classification
"""
from enum import Enum
from typing import Tuple


class IntentType(Enum):
    """Question intent categories"""
    CONCEPTUAL = "conceptual"  # What is X? Explain Y
    TECHNICAL = "technical"    # How does X work? Implementation details
    PDF_BASED = "pdf_based"    # Questions about loaded PDF content
    SYSTEM = "system"          # Commands like load, help, exit


class IntentDetector:
    """Detects user intent from CLI input"""
    
    # Keywords for intent classification
    CONCEPTUAL_KEYWORDS = [
        "what is", "define", "explain", "describe", "meaning of",
        "concept of", "introduction to", "overview of"
    ]
    
    TECHNICAL_KEYWORDS = [
        "how to", "implement", "code", "algorithm", "steps to",
        "procedure", "process", "method", "technique", "approach"
    ]
    
    SYSTEM_COMMANDS = {
        "load": "load_pdf",
        "help": "show_help",
        "exit": "exit_app",
        "quit": "exit_app",
        "status": "show_status",
        "clear": "clear_context"
    }
    
    def detect(self, user_input: str) -> Tuple[IntentType, str]:
        """
        Detect intent from user input
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Tuple of (IntentType, processed_query)
        """
        user_input = user_input.strip()
        lower_input = user_input.lower()
        
        # Check for system commands
        first_word = lower_input.split()[0] if lower_input else ""
        if first_word in self.SYSTEM_COMMANDS:
            return IntentType.SYSTEM, user_input
        
        # Check for conceptual questions
        if any(kw in lower_input for kw in self.CONCEPTUAL_KEYWORDS):
            return IntentType.CONCEPTUAL, user_input
        
        # Check for technical questions
        if any(kw in lower_input for kw in self.TECHNICAL_KEYWORDS):
            return IntentType.TECHNICAL, user_input
        
        # Default to PDF-based if PDF is loaded
        return IntentType.PDF_BASED, user_input
    
    def is_system_command(self, user_input: str) -> Tuple[bool, str]:
        """
        Check if input is a system command
        
        Args:
            user_input: User input string
            
        Returns:
            Tuple of (is_command, command_name)
        """
        first_word = user_input.strip().lower().split()[0] if user_input.strip() else ""
        if first_word in self.SYSTEM_COMMANDS:
            return True, self.SYSTEM_COMMANDS[first_word]
        return False, ""
