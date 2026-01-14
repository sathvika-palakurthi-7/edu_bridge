"""
EduBridge Setup Verification Script
Run this to verify your installation is correct
"""
import sys
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"[OK] Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"[FAIL] Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        "langchain",
        "langchain_community",
        "langchain_ollama",
        "chromadb",
        "pypdf",
        "sentence_transformers",
        "dotenv"
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"[OK] {package} - Installed")
        except ImportError:
            print(f"[FAIL] {package} - Missing")
            missing.append(package)
    
    return len(missing) == 0

def check_ollama():
    """Check Ollama connectivity"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            print("[OK] Ollama - Running")
            
            # Check for model
            data = response.json()
            models = [m['name'] for m in data.get('models', [])]
            if any('llama3.2:1b' in m for m in models):
                print("[OK] llama3.2:1b - Available")
                return True
            else:
                print("[FAIL] llama3.2:1b - Not found")
                print("  Run: ollama pull llama3.2:1b")
                return False
        else:
            print("[FAIL] Ollama - Not responding")
            return False
    except Exception as e:
        print("[FAIL] Ollama - Not running")
        print("  Run: ollama serve")
        return False

def check_ocr():
    """Check if Tesseract OCR is available"""
    import pytesseract
    from PIL import Image
    import os
    
    # Check default path
    default_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    if os.path.exists(default_path):
        print(f"[OK] Tesseract binary found at {default_path}")
        pytesseract.pytesseract.tesseract_cmd = default_path
    
    try:
        version = pytesseract.get_tesseract_version()
        print(f"[OK] Tesseract OCR v{version} - Ready")
        return True
    except Exception as e:
        print(f"[FAIL] Tesseract OCR not detected: {e}")
        return False

def check_project_structure():
    """Check project structure"""
    base_dir = Path(__file__).parent
    required_files = [
        "src/config.py",
        "src/pdf_processor.py",
        "src/intent_detector.py",
        "src/ai_tutor.py",
        "src/cli.py",
        "main.py",
        "requirements.txt",
        ".env"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"[OK] {file_path} - Found")
        else:
            print(f"[FAIL] {file_path} - Missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks"""
    print("="*60)
    print("EDUBRIDGE SETUP VERIFICATION")
    print("="*60)
    
    print("\n[1/4] Checking Python Version...")
    python_ok = check_python_version()
    
    print("\n[2/4] Checking Dependencies...")
    deps_ok = check_dependencies()
    
    print("\n[3/5] Checking Ollama...")
    ollama_ok = check_ollama()

    print("\n[4/5] Checking OCR Support...")
    ocr_ok = check_ocr()
    
    print("\n[5/5] Checking Project Structure...")
    structure_ok = check_project_structure()
    
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    if python_ok and deps_ok and ollama_ok and structure_ok:
        print("[SUCCESS] All checks passed!")
        if not ocr_ok:
            print("[INFO] Note: OCR is missing, but system will still work for text-based PDFs.")
        print("\nYou can now run: python main.py")
    else:
        print("[WARNING] Some checks failed. Please fix the issues above.")
        
        if not deps_ok:
            print("\nTo install dependencies:")
            print("  pip install -r requirements.txt")
        
        if not ollama_ok:
            print("\nTo setup Ollama:")
            print("  1. Download from https://ollama.ai")
            print("  2. Run: ollama serve")
            print("  3. Run: ollama pull llama3.2:1b")
    
    print("="*60)

if __name__ == "__main__":
    main()
