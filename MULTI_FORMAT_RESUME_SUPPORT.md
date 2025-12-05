# Multi-Format Resume Upload Support

## Overview
Added support for uploading resumes in multiple file formats: PDF, Word documents (.docx), and plain text files (.txt). Previously, only PDF files were supported.

## Changes Made

### 1. Dependencies (`requirements.txt`)
- Added `python-docx>=1.0.0` for parsing Word documents
- This library enables extraction of text from DOCX files including paragraphs and tables

### 2. Resume Parser (`src/parsers/resume_parser.py`)
Added new parsing methods to handle multiple file formats:

#### New Methods:
- **`parse_docx(docx_path: str) -> ResumeData`**: Parse DOCX files from file path
- **`parse_docx_bytes(docx_bytes: bytes) -> ResumeData`**: Parse DOCX files from bytes
- **`parse_txt(txt_path: str) -> ResumeData`**: Parse plain text files from file path
- **`parse_txt_bytes(txt_bytes: bytes) -> ResumeData`**: Parse plain text files from bytes
- **`parse_resume_bytes(file_bytes: bytes, file_name: str) -> ResumeData`**: Unified method that auto-detects file format based on file extension and parses accordingly

#### Features:
- All parsing methods extract the same information:
  - Raw text content
  - Candidate name
  - Email address
  - Technical skills
- DOCX parser also extracts text from tables
- Proper error handling for unsupported formats and parsing failures
- Comprehensive logging for debugging

### 3. API Layer (`src/api/main.py`)
Updated both file upload endpoints to support multiple formats:

#### Endpoints Modified:
- **`POST /api/v1/generate-questions`**: Now accepts PDF, DOCX, or TXT files
- **`POST /api/v1/parse-resume`**: Now accepts PDF, DOCX, or TXT files

#### Changes:
- Updated file validation to check for `.pdf`, `.docx`, or `.txt` extensions
- Changed resume parsing to use the new `parse_resume_bytes()` method
- Updated error messages to reflect supported formats
- Updated API documentation strings

### 4. Frontend HTML (`templates/index.html`)
Updated the resume upload UI:
- Changed label from "Upload Resume (PDF)" to "Upload Resume (PDF, DOCX, or TXT)"
- Updated file input `accept` attribute to `.pdf,.docx,.txt`
- Updated placeholder text from "PDF files only" to "PDF, DOCX, or TXT files"

### 5. Frontend JavaScript

#### In HTML Template (`templates/index.html`):
- Updated drag-and-drop validation to accept multiple MIME types:
  - `application/pdf`
  - `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (DOCX)
  - `text/plain`
- Also checks file extensions as fallback: `.pdf`, `.docx`, `.txt`

#### In External Script (`static/js/app.js`):
Updated `handleFileSelection()` method:
- Added support for DOCX MIME type detection
- Added fallback file extension checking
- Updated error messages to reference all supported formats
- Maintains 10MB file size limit for all formats

## Supported File Formats

| Format | Extension | MIME Type | Status |
|--------|-----------|-----------|--------|
| PDF | `.pdf` | `application/pdf` | ✅ Supported |
| Word Document | `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | ✅ Supported |
| Plain Text | `.txt` | `text/plain` | ✅ Supported |

## Installation

To use the new multi-format support, install the updated dependencies:

```bash
pip install -r requirements.txt
```

Or install just the new dependency:

```bash
pip install python-docx>=1.0.0
```

## Usage

### REST API Examples

#### Generate questions from DOCX resume:
```bash
curl -X POST "http://localhost:8000/api/v1/generate-questions" \
  -F "resume=@resume.docx" \
  -F "job_description=Senior Python Developer..." \
  -F "round_type=technical" \
  -F "difficulty=intermediate" \
  -F "num_questions=10" \
  -F "api_key=YOUR_API_KEY"
```

#### Generate questions from TXT resume:
```bash
curl -X POST "http://localhost:8000/api/v1/generate-questions" \
  -F "resume=@resume.txt" \
  -F "job_description=Senior Python Developer..." \
  -F "round_type=technical" \
  -F "difficulty=intermediate" \
  -F "num_questions=10" \
  -F "api_key=YOUR_API_KEY"
```

#### Parse resume (any format):
```bash
curl -X POST "http://localhost:8000/api/v1/parse-resume" \
  -F "resume=@resume.docx"
```

### Python API Examples

```python
from src.parsers import ResumeParser

parser = ResumeParser()

# Parse DOCX file
resume_data = parser.parse_docx("resume.docx")

# Parse TXT file
resume_data = parser.parse_txt("resume.txt")

# Parse any format automatically (recommended)
resume_data = parser.parse_resume_bytes(file_bytes, "resume.docx")

print(f"Name: {resume_data.name}")
print(f"Email: {resume_data.email}")
print(f"Skills: {resume_data.skills}")
```

## Backward Compatibility

All changes are fully backward compatible:
- Existing PDF functionality is preserved and unchanged
- The new unified `parse_resume_bytes()` method handles PDF files correctly
- No breaking changes to the API contracts or response formats

## Testing Recommendations

To verify the implementation works correctly:

1. **Test PDF uploads** - Verify existing functionality still works
2. **Test DOCX uploads** - Upload a Word document resume
3. **Test TXT uploads** - Upload a plain text resume
4. **Test error handling** - Try uploading unsupported formats (e.g., .doc, .pages, .pdf.txt)
5. **Test drag-and-drop** - Ensure all formats work with drag-and-drop UI
6. **Test via API** - Use curl or API client to test all endpoints
7. **Test file size limits** - Verify 10MB limit is enforced for all formats

## Future Enhancements

Possible improvements for future versions:
- Support for `.doc` format (older Word documents)
- Support for `.odt` format (OpenDocument Text)
- Support for `.rtf` format (Rich Text Format)
- Improved text extraction from complex document layouts
- OCR support for scanned documents
- Better table parsing from DOCX files

## Notes

- DOCX text extraction includes both paragraphs and table content
- TXT files are decoded as UTF-8; other encodings may cause issues
- File size limit of 10MB applies to all formats
- All parsing methods return the same `ResumeData` object structure
- Error messages clearly indicate which formats are supported
