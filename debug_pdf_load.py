"""
Debug script to verify PDF loading for a specific file
"""
import sys
import os
# Ensure src is in python path
sys.path.append(os.getcwd())

from src.pdf_processor import PDFProcessor
from src.config import Config

def test_load():
    pdf_path = r"N:\Sathvika\EDUBRIDGE\src\syllabus\AI_Agents_1761113188.pdf"
    print(f"Testing load for: {pdf_path}")
    
    processor = PDFProcessor()
    success = processor.load_pdf(pdf_path)
    
    if success:
        print("\nSUCCESS: PDF loaded correctly")
        print(f"Current PDF: {processor.get_current_pdf()}")
        if processor.vectorstore:
            # Basic collection stats if accessible, or just confirm it exists
            print("Vectorstore created successfully")
    else:
        print("\nFAILURE: Could not load PDF")

if __name__ == "__main__":
    test_load()
