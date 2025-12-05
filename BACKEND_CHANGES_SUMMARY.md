# Backend Changes - Multi-Format Resume Support

## ✅ YES - We Made Comprehensive Backend Changes!

Here's a detailed breakdown of all backend modifications for DOCX and TXT support:

---

## 1. Resume Parser (`src/parsers/resume_parser.py`)

### Import Changes
```python
# ADDED:
from docx import Document
```

### New Methods Added (5 total)

#### ✅ Method 1: `parse_docx(docx_path: str) -> ResumeData`
- **Purpose**: Parse DOCX files from file path
- **Features**:
  - Extracts text from all paragraphs
  - Extracts text from tables (if any)
  - Validates file exists
  - Returns structured ResumeData with name, email, skills
  - Comprehensive error handling and logging

```python
def parse_docx(self, docx_path: str) -> ResumeData:
    """Parse a DOCX (Word) resume and extract text content."""
    # Validates file exists
    # Uses python-docx library to read document
    # Iterates through paragraphs AND tables
    # Extracts name, email, skills
    # Returns ResumeData object
```

#### ✅ Method 2: `parse_docx_bytes(docx_bytes: bytes) -> ResumeData`
- **Purpose**: Parse DOCX files from bytes (for file uploads)
- **Features**:
  - Handles binary data from HTTP uploads
  - Same extraction logic as parse_docx
  - Uses BytesIO for in-memory parsing
  - No file I/O required

```python
def parse_docx_bytes(self, docx_bytes: bytes) -> ResumeData:
    """Parse a DOCX resume from bytes."""
    # Creates BytesIO object from bytes
    # Uses Document(BytesIO) for in-memory parsing
    # Extracts paragraphs and tables
    # Returns ResumeData object
```

#### ✅ Method 3: `parse_txt(txt_path: str) -> ResumeData`
- **Purpose**: Parse plain text files from file path
- **Features**:
  - Reads UTF-8 encoded text files
  - Validates file exists
  - Extracts name, email, skills from text
  - Returns structured ResumeData

```python
def parse_txt(self, txt_path: str) -> ResumeData:
    """Parse a TXT resume and extract text content."""
    # Opens file with UTF-8 encoding
    # Reads entire file content
    # Extracts structured data
    # Returns ResumeData object
```

#### ✅ Method 4: `parse_txt_bytes(txt_bytes: bytes) -> ResumeData`
- **Purpose**: Parse text files from bytes (for file uploads)
- **Features**:
  - Decodes bytes as UTF-8
  - Extracts name, email, skills
  - Returns structured ResumeData

```python
def parse_txt_bytes(self, txt_bytes: bytes) -> ResumeData:
    """Parse a TXT resume from bytes."""
    # Decodes bytes to UTF-8 string
    # Extracts name, email, skills
    # Returns ResumeData object
```

#### ✅ Method 5: `parse_resume_bytes(file_bytes: bytes, file_name: str) -> ResumeData`
- **Purpose**: Universal parser with automatic format detection
- **Features**:
  - Auto-detects format by file extension
  - Routes to appropriate parser method
  - Single entry point for all formats
  - Clear error for unsupported formats

```python
def parse_resume_bytes(self, file_bytes: bytes, file_name: str) -> ResumeData:
    """Parse a resume from bytes, automatically detecting the file format."""
    # Checks file_name extension
    # if .pdf -> calls parse_pdf_bytes()
    # elif .docx -> calls parse_docx_bytes()
    # elif .txt -> calls parse_txt_bytes()
    # else -> raises ValueError for unsupported format
    # Returns ResumeData object
```

### Existing Methods (Unchanged)
- `parse_pdf()` - Still works exactly as before
- `parse_pdf_bytes()` - Still works exactly as before
- `_extract_email()` - Reused for all formats
- `_extract_name()` - Reused for all formats
- `_extract_skills()` - Reused for all formats

---

## 2. API Layer (`src/api/main.py`)

### Endpoint 1: `POST /api/v1/generate-questions`

**Changes:**
- Updated parameter description: "Resume file (PDF, DOCX, or TXT)"
- Updated file validation logic:
  ```python
  supported_formats = ['.pdf', '.docx', '.txt']
  file_lower = resume.filename.lower()
  if not any(file_lower.endswith(fmt) for fmt in supported_formats):
      raise HTTPException(
          status_code=400,
          detail="Only PDF, DOCX, and TXT files are supported for resumes"
      )
  ```
- Changed resume parser call:
  ```python
  # OLD:
  resume_data = resume_parser.parse_pdf_bytes(resume_bytes)
  
  # NEW:
  resume_data = resume_parser.parse_resume_bytes(resume_bytes, resume.filename)
  ```
- Updated docstring to reflect all supported formats

### Endpoint 2: `POST /api/v1/parse-resume`

**Changes:**
- Updated parameter description: "Resume file (PDF, DOCX, or TXT)"
- Updated file validation logic (same as above)
- Changed resume parser call to use universal method:
  ```python
  # OLD:
  if not resume.filename.lower().endswith('.pdf'):
      raise HTTPException(...)
  resume_data = resume_parser.parse_pdf_bytes(resume_bytes)
  
  # NEW:
  supported_formats = ['.pdf', '.docx', '.txt']
  if not any(file_lower.endswith(fmt) for fmt in supported_formats):
      raise HTTPException(...)
  resume_data = resume_parser.parse_resume_bytes(resume_bytes, resume.filename)
  ```
- Updated docstring to reflect all supported formats

---

## 3. Dependencies (`requirements.txt`)

### Added
```
# Word Document Processing
python-docx>=1.0.0
```

This is the library that enables DOCX file parsing.

---

## Data Flow for Each Format

### PDF Upload Flow
```
User uploads .pdf
    ↓
API validates .pdf extension ✓
    ↓
resume_parser.parse_resume_bytes() called with filename
    ↓
File extension check → endswith('.pdf') ✓
    ↓
parse_pdf_bytes() executed
    ↓
pdfplumber extracts text
    ↓
_extract_name(), _extract_email(), _extract_skills() called
    ↓
ResumeData returned with all fields
```

### DOCX Upload Flow
```
User uploads .docx
    ↓
API validates .docx extension ✓
    ↓
resume_parser.parse_resume_bytes() called with filename
    ↓
File extension check → endswith('.docx') ✓
    ↓
parse_docx_bytes() executed
    ↓
python-docx Document() reads BytesIO
    ↓
Extracts from paragraphs + tables
    ↓
_extract_name(), _extract_email(), _extract_skills() called
    ↓
ResumeData returned with all fields
```

### TXT Upload Flow
```
User uploads .txt
    ↓
API validates .txt extension ✓
    ↓
resume_parser.parse_resume_bytes() called with filename
    ↓
File extension check → endswith('.txt') ✓
    ↓
parse_txt_bytes() executed
    ↓
Decodes bytes as UTF-8
    ↓
_extract_name(), _extract_email(), _extract_skills() called
    ↓
ResumeData returned with all fields
```

---

## Error Handling

### File Validation Errors
```python
# Unsupported format
{
    "detail": "Only PDF, DOCX, and TXT files are supported for resumes"
}
```

### Parsing Errors
```python
# Empty file
Exception: "Failed to parse resume: No text could be extracted from the [format] file"

# Corrupted file
Exception: "Failed to parse resume: [specific error message]"

# File I/O error
FileNotFoundError: "Resume file not found: [path]"
```

---

## Logging

All parsing operations are logged:
```
INFO: Successfully parsed resume: resume.pdf
INFO: Successfully parsed resume from bytes
ERROR: Error parsing DOCX resume.docx: [error details]
```

---

## Backend Architecture Summary

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Endpoints                    │
│  /api/v1/generate-questions  │  /api/v1/parse-resume   │
└──────────────┬────────────────────────────┬──────────────┘
               │                            │
               └──────────────┬─────────────┘
                              │
                    ┌─────────▼────────────┐
                    │ ResumeParser         │
                    │ parse_resume_bytes() │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────────┐
                    │                         │
        ┌───────────▼────────────┐   ┌──────▼──────────────┐
        │ File Format Detection   │   │ Existing Methods    │
        │ (by file extension)     │   │ (Reused for all)    │
        └───────────┬─────────────┘   │                     │
                    │                 │ • _extract_name()   │
        ┌───────────┴─────────────┐   │ • _extract_email()  │
        │                         │   │ • _extract_skills() │
   ┌────▼────┐  ┌────────┐  ┌────▼───┴──────────────────────┘
   │ .pdf    │  │ .docx  │  │ .txt
   │         │  │        │  │
   │  PDF    │  │ DOCX   │  │ TXT
   │ Parser  │  │Parser  │  │Parser
   │         │  │        │  │
   └────┬────┘  └────┬───┘  └────┬─────┐
        │            │           │     │
   pdfplumber  python-docx    UTF-8  ┌─▼─────────────────────┐
   (existing)   (NEW)          (NEW) │ Returns ResumeData:   │
                                     │ • raw_text            │
                            ┌────────┤ • name                │
                            │        │ • email               │
                            │        │ • skills              │
                            │        └──────────────────────┘
                            │
                       ┌────▼──────────────┐
                       │ Return to API     │
                       │ → JSON Response   │
                       └───────────────────┘
```

---

## Summary of Backend Enhancements

| Component | Change Type | Details |
|-----------|-------------|---------|
| Dependencies | Added | `python-docx>=1.0.0` |
| ResumeParser | Extended | 5 new methods added |
| API Endpoints | Updated | 2 endpoints enhanced |
| File Support | Expanded | PDF + DOCX + TXT |
| Error Handling | Enhanced | Clear messages for all formats |
| Logging | Enhanced | Detailed logs for debugging |
| Backward Compatibility | Maintained | All existing functionality preserved |

---

## Testing the Backend

```bash
# Test parse DOCX endpoint
curl -X POST "http://localhost:8000/api/v1/parse-resume" \
  -F "resume=@resume.docx"

# Test generate-questions with TXT
curl -X POST "http://localhost:8000/api/v1/generate-questions" \
  -F "resume=@resume.txt" \
  -F "job_description=Python Developer" \
  -F "round_type=technical" \
  -F "api_key=YOUR_KEY"
```

---

✅ **All backend changes complete and production-ready!**
