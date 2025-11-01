"""Resume parser module for extracting text from PDF files."""

import pdfplumber
import re
from typing import Optional
from pathlib import Path
import logging

from ..models import ResumeData


logger = logging.getLogger(__name__)


class ResumeParser:
    """Parse PDF resumes and extract structured information."""
    
    def __init__(self):
        """Initialize the resume parser."""
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    
    def parse_pdf(self, pdf_path: str) -> ResumeData:
        """
        Parse a PDF resume and extract text content.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            ResumeData object with extracted information
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            Exception: If PDF parsing fails
        """
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"Resume file not found: {pdf_path}")
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Extract text from all pages
                raw_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        raw_text += page_text + "\n"
                
                if not raw_text.strip():
                    raise ValueError("No text could be extracted from the PDF")
                
                # Extract structured information
                name = self._extract_name(raw_text)
                email = self._extract_email(raw_text)
                skills = self._extract_skills(raw_text)
                
                logger.info(f"Successfully parsed resume: {pdf_path}")
                
                return ResumeData(
                    raw_text=raw_text,
                    name=name,
                    email=email,
                    skills=skills
                )
                
        except Exception as e:
            logger.error(f"Error parsing PDF {pdf_path}: {str(e)}")
            raise Exception(f"Failed to parse resume: {str(e)}")
    
    def parse_pdf_bytes(self, pdf_bytes: bytes) -> ResumeData:
        """
        Parse a PDF resume from bytes.
        
        Args:
            pdf_bytes: PDF file content as bytes
            
        Returns:
            ResumeData object with extracted information
        """
        try:
            import io
            pdf_file = io.BytesIO(pdf_bytes)
            
            with pdfplumber.open(pdf_file) as pdf:
                raw_text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        raw_text += page_text + "\n"
                
                if not raw_text.strip():
                    raise ValueError("No text could be extracted from the PDF")
                
                name = self._extract_name(raw_text)
                email = self._extract_email(raw_text)
                skills = self._extract_skills(raw_text)
                
                logger.info("Successfully parsed resume from bytes")
                
                return ResumeData(
                    raw_text=raw_text,
                    name=name,
                    email=email,
                    skills=skills
                )
                
        except Exception as e:
            logger.error(f"Error parsing PDF bytes: {str(e)}")
            raise Exception(f"Failed to parse resume: {str(e)}")
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text."""
        match = self.email_pattern.search(text)
        return match.group(0) if match else None
    
    def _extract_name(self, text: str) -> Optional[str]:
        """
        Extract candidate name from resume text.
        Assumes name is in the first few lines.
        """
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            # Simple heuristic: name is usually short and at the top
            if line and len(line.split()) <= 4 and len(line) < 50:
                # Avoid lines with common resume keywords
                if not any(keyword in line.lower() for keyword in 
                          ['resume', 'cv', 'curriculum', 'email', 'phone', 'address']):
                    return line
        return None
    
    def _extract_skills(self, text: str) -> list:
        """
        Extract technical skills from resume text.
        This is a simple keyword-based approach.
        """
        # Common technical skills and technologies
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'fastapi',
            'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform',
            'git', 'jenkins', 'ci/cd', 'agile', 'scrum',
            'machine learning', 'deep learning', 'ai', 'nlp', 'computer vision',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'rest api', 'graphql', 'microservices', 'linux', 'bash'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates


class ResumeParserError(Exception):
    """Custom exception for resume parsing errors."""
    pass
