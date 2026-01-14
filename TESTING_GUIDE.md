# EduBridge Testing Guide

## 🧪 Testing Strategy

This guide provides comprehensive test cases to validate EduBridge functionality.

---

## Pre-Testing Checklist

Before running tests, ensure:

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Ollama model pulled (`ollama pull llama3.2:1b`)
- [ ] Ollama is running (`ollama list`)
- [ ] Verification passed (`python verify_setup.py`)

---

## Test Suite

### Test 1: Application Launch

**Objective**: Verify application starts correctly

**Steps**:
```powershell
python main.py
```

**Expected Output**:
```
╔═══════════════════════════════════════════════════════════╗
║                    EDUBRIDGE AI TUTOR                     ║
║          AI-Powered Skilling & Learning System            ║
╚═══════════════════════════════════════════════════════════╝

Type 'help' for available commands

[OK] Ollama connection successful

EduBridge>
```

**Pass Criteria**:
- ✅ Banner displays correctly
- ✅ Ollama connection successful
- ✅ Prompt appears
- ✅ No error messages

**Status**: ⏳ PENDING

---

### Test 2: Help Command

**Objective**: Verify help system works

**Steps**:
```
EduBridge> help
```

**Expected Output**:
```
AVAILABLE COMMANDS:
-------------------
load <pdf_path>     Load a PDF document for tutoring
status              Show current system status
help                Show this help message
exit/quit           Exit the application
...
```

**Pass Criteria**:
- ✅ Help text displays
- ✅ All commands listed
- ✅ Format is readable

**Status**: ⏳ PENDING

---

### Test 3: Status Command (No PDF)

**Objective**: Check status before loading PDF

**Steps**:
```
EduBridge> status
```

**Expected Output**:
```
SYSTEM STATUS:
----------------------------------------
PDF Loaded     : None
Model          : llama3.2:1b
Ollama URL     : http://localhost:11434
Status         : No PDF loaded
----------------------------------------
```

**Pass Criteria**:
- ✅ Status displays correctly
- ✅ Shows "No PDF loaded"
- ✅ Model name correct
- ✅ Ollama URL correct

**Status**: ⏳ PENDING

---

### Test 4: PDF Loading

**Objective**: Verify PDF loading functionality

**Steps**:
```
EduBridge> load "Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf"
```

**Expected Output**:
```
Loading PDF: Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf
Please wait...
Successfully loaded: Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf
Pages processed: [X]
Chunks created: [X]

[SUCCESS] PDF loaded successfully
You can now ask questions about this document
```

**Pass Criteria**:
- ✅ PDF loads without errors
- ✅ Page count displayed
- ✅ Chunk count displayed
- ✅ Success message shown

**Status**: ⏳ PENDING

---

### Test 5: Status Command (After PDF Load)

**Objective**: Verify status updates after PDF load

**Steps**:
```
EduBridge> status
```

**Expected Output**:
```
SYSTEM STATUS:
----------------------------------------
PDF Loaded     : Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf
Model          : llama3.2:1b
Ollama URL     : http://localhost:11434
Status         : Ready
----------------------------------------
```

**Pass Criteria**:
- ✅ Shows loaded PDF name
- ✅ Status changed to "Ready"

**Status**: ⏳ PENDING

---

### Test 6: Conceptual Question

**Objective**: Test answering conceptual questions

**Steps**:
```
EduBridge> What is project documentation?
```

**Expected Output Format**:
```
Processing question...

============================================================
Answer: [Direct answer from PDF]
Explanation: [Step-by-step breakdown]
Source: [Page X]
============================================================
```

**Pass Criteria**:
- ✅ Answer provided
- ✅ Explanation included
- ✅ Source page number shown
- ✅ Response time < 10 seconds
- ✅ Answer is relevant to question

**Status**: ⏳ PENDING

---

### Test 7: Technical Question

**Objective**: Test answering technical questions

**Steps**:
```
EduBridge> How should a fresher explain their project?
```

**Expected Output Format**:
```
Processing question...

============================================================
Answer: [Practical steps/approach from PDF]
Explanation: [Detailed breakdown]
Source: [Page X]
============================================================
```

**Pass Criteria**:
- ✅ Technical answer provided
- ✅ Step-by-step explanation
- ✅ Source attribution
- ✅ Answer is actionable

**Status**: ⏳ PENDING

---

### Test 8: Specific Detail Question

**Objective**: Test retrieval of specific information

**Steps**:
```
EduBridge> What are the key components of project documentation?
```

**Expected Output**:
- List or description of components
- Source page reference
- Relevant explanation

**Pass Criteria**:
- ✅ Specific details extracted
- ✅ Accurate to PDF content
- ✅ Complete answer

**Status**: ⏳ PENDING

---

### Test 9: Out-of-Scope Question

**Objective**: Verify "Not Found" response for irrelevant questions

**Steps**:
```
EduBridge> What is quantum computing?
```

**Expected Output**:
```
Processing question...

============================================================
Not Found
============================================================
```

**Pass Criteria**:
- ✅ Returns exactly "Not Found"
- ✅ No hallucinated answer
- ✅ No made-up information

**Status**: ⏳ PENDING

---

### Test 10: Question Without PDF

**Objective**: Verify error handling when no PDF loaded

**Steps**:
1. Exit and restart application
2. Ask question without loading PDF:
```
EduBridge> What is project management?
```

**Expected Output**:
```
Processing question...

============================================================
Need to validate: No PDF loaded. Use 'load <pdf_path>' command first.
============================================================
```

**Pass Criteria**:
- ✅ Error message displayed
- ✅ Instructs to load PDF
- ✅ No crash

**Status**: ⏳ PENDING

---

### Test 11: Invalid PDF Path

**Objective**: Test error handling for invalid file paths

**Steps**:
```
EduBridge> load "nonexistent.pdf"
```

**Expected Output**:
```
Loading PDF: nonexistent.pdf
Please wait...
Error: PDF file not found at nonexistent.pdf

[FAILED] Failed to load PDF
```

**Pass Criteria**:
- ✅ Error message displayed
- ✅ No crash
- ✅ Returns to prompt

**Status**: ⏳ PENDING

---

### Test 12: Multiple Questions in Sequence

**Objective**: Test handling multiple questions

**Steps**:
```
EduBridge> load "Sample document of How a Fresher Should Explain and prepare Project Documentation.pdf"
EduBridge> What is project documentation?
EduBridge> How should a fresher prepare documentation?
EduBridge> What are the benefits of good documentation?
```

**Pass Criteria**:
- ✅ All questions answered
- ✅ No performance degradation
- ✅ Consistent response format
- ✅ No memory issues

**Status**: ⏳ PENDING

---

### Test 13: Exit Command

**Objective**: Verify clean application exit

**Steps**:
```
EduBridge> exit
```

**Expected Output**:
```
Exiting EduBridge...
```

**Pass Criteria**:
- ✅ Clean exit
- ✅ No errors
- ✅ Returns to shell

**Status**: ⏳ PENDING

---

### Test 14: Quit Command

**Objective**: Verify alternative exit command

**Steps**:
```
EduBridge> quit
```

**Expected Output**:
```
Exiting EduBridge...
```

**Pass Criteria**:
- ✅ Same as exit command
- ✅ Clean termination

**Status**: ⏳ PENDING

---

### Test 15: Keyboard Interrupt (Ctrl+C)

**Objective**: Test graceful handling of Ctrl+C

**Steps**:
1. Start application
2. Press Ctrl+C

**Expected Output**:
```
Exiting EduBridge...
```

**Pass Criteria**:
- ✅ Graceful exit
- ✅ No stack trace
- ✅ Clean shutdown

**Status**: ⏳ PENDING

---

## Advanced Tests

### Test 16: Long Question

**Objective**: Test handling of lengthy questions

**Steps**:
```
EduBridge> Can you explain in detail what are all the important aspects that a fresher should consider when preparing project documentation for an interview, including the structure, content, and presentation style?
```

**Pass Criteria**:
- ✅ Handles long input
- ✅ Provides comprehensive answer
- ✅ No truncation issues

**Status**: ⏳ PENDING

---

### Test 17: Ambiguous Question

**Objective**: Test handling of vague questions

**Steps**:
```
EduBridge> Tell me about projects
```

**Expected**: 
- Either relevant answer from PDF
- Or "Not Found" if too vague

**Pass Criteria**:
- ✅ No crash
- ✅ Valid response format

**Status**: ⏳ PENDING

---

### Test 18: Repeated Question

**Objective**: Test consistency of answers

**Steps**:
```
EduBridge> What is project documentation?
[Note the answer]
EduBridge> What is project documentation?
[Compare answers]
```

**Pass Criteria**:
- ✅ Answers are consistent
- ✅ Same source page
- ✅ Similar content

**Status**: ⏳ PENDING

---

### Test 19: Case Sensitivity

**Objective**: Test case-insensitive question handling

**Steps**:
```
EduBridge> what is PROJECT DOCUMENTATION?
EduBridge> What Is Project Documentation?
```

**Pass Criteria**:
- ✅ Both questions work
- ✅ Similar answers
- ✅ Case doesn't affect results

**Status**: ⏳ PENDING

---

### Test 20: Empty Input

**Objective**: Test handling of empty input

**Steps**:
```
EduBridge> [Press Enter without typing]
```

**Expected**:
- Returns to prompt without error

**Pass Criteria**:
- ✅ No crash
- ✅ Prompt reappears

**Status**: ⏳ PENDING

---

## Performance Tests

### Test 21: Response Time

**Objective**: Measure response times

**Metrics to Track**:
- PDF loading time: _______ seconds
- First question: _______ seconds
- Subsequent questions: _______ seconds

**Acceptable Ranges**:
- PDF loading: < 30 seconds
- Questions: < 10 seconds

**Status**: ⏳ PENDING

---

### Test 22: Memory Usage

**Objective**: Monitor memory consumption

**Steps**:
1. Check Task Manager before starting
2. Load PDF
3. Ask 10 questions
4. Check memory usage

**Acceptable**:
- < 2GB RAM usage

**Status**: ⏳ PENDING

---

## Integration Tests

### Test 23: Vector Store Persistence

**Objective**: Verify vector store is created

**Steps**:
1. Load PDF
2. Check `data/vectorstore` directory
3. Verify files created

**Expected**:
- `chroma.sqlite3` file exists
- Embedding files present

**Pass Criteria**:
- ✅ Vector store directory created
- ✅ Database files present

**Status**: ⏳ PENDING

---

### Test 24: Ollama Communication

**Objective**: Verify Ollama integration

**Steps**:
1. Stop Ollama: `ollama stop` (if possible)
2. Try to start EduBridge
3. Observe warning message

**Expected**:
```
[WARNING] Cannot connect to Ollama
  Make sure Ollama is running at http://localhost:11434
```

**Pass Criteria**:
- ✅ Warning displayed
- ✅ Application doesn't crash
- ✅ Can still access other commands

**Status**: ⏳ PENDING

---

## Test Results Summary

### Overall Status

```
Total Tests: 24
Passed: ___
Failed: ___
Pending: ___
Success Rate: ___%
```

### Critical Tests (Must Pass)

- [ ] Test 1: Application Launch
- [ ] Test 4: PDF Loading
- [ ] Test 6: Conceptual Question
- [ ] Test 9: Out-of-Scope Question
- [ ] Test 13: Exit Command

### Important Tests (Should Pass)

- [ ] Test 7: Technical Question
- [ ] Test 10: Question Without PDF
- [ ] Test 11: Invalid PDF Path
- [ ] Test 12: Multiple Questions

### Nice-to-Have Tests

- [ ] Test 15: Keyboard Interrupt
- [ ] Test 21: Response Time
- [ ] Test 22: Memory Usage

---

## Bug Report Template

If any test fails, document using this template:

```
Test Number: ___
Test Name: ___
Expected: ___
Actual: ___
Steps to Reproduce:
1. 
2. 
3. 

Error Message (if any):
___

Screenshots/Logs:
___
```

---

## Testing Checklist

### Before Testing
- [ ] Read all test descriptions
- [ ] Prepare test environment
- [ ] Have PDF ready
- [ ] Ollama running

### During Testing
- [ ] Follow steps exactly
- [ ] Note response times
- [ ] Document any errors
- [ ] Take screenshots if needed

### After Testing
- [ ] Fill in test results
- [ ] Calculate success rate
- [ ] Report any bugs
- [ ] Suggest improvements

---

## Success Criteria

**Minimum Viable Product**:
- All Critical Tests pass (100%)
- At least 80% of Important Tests pass
- No crashes or data loss

**Production Ready**:
- All Critical Tests pass (100%)
- All Important Tests pass (100%)
- At least 70% of Nice-to-Have Tests pass

---

## Next Steps After Testing

If all tests pass:
✅ System is ready for use
✅ Start using with real PDFs
✅ Explore advanced features

If tests fail:
❌ Review error messages
❌ Check INSTALL.md for troubleshooting
❌ Run `python verify_setup.py`
❌ Verify dependencies

---

**Happy Testing! 🧪**
