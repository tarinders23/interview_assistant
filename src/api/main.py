"""FastAPI application for the Interview Assistant."""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
from typing import Optional, List
import os

from ..agent import InterviewQuestionAgent, InterviewAgentError
from ..parsers import ResumeParser, ResumeParserError
from ..models import (
    QuestionGenerationRequest,
    QuestionGenerationResponse,
    RoundType,
    DifficultyLevel
)
from ..config import settings


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(
    title="Interview Assistant API",
    description="AI-powered interview question generator",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files and templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize services
resume_parser = ResumeParser()


@app.get("/", response_class=HTMLResponse)
async def web_home(request: Request):
    """Serve the main web interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api")
async def api_root():
    """API root endpoint with API information."""
    return {
        "message": "Interview Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model": settings.model_name
    }


@app.post("/api/v1/generate-questions", response_model=QuestionGenerationResponse)
async def generate_questions_from_upload(
    resume: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    job_description: Optional[str] = Form(None, description="Job description text"),
    job_description_file: Optional[UploadFile] = File(None, description="Job description file (PDF or DOCX)"),
    round_type: RoundType = Form(..., description="Interview round type"),
    difficulty: DifficultyLevel = Form(
        DifficultyLevel.INTERMEDIATE,
        description="Question difficulty level"
    ),
    num_questions: int = Form(10, ge=1, le=50, description="Number of questions"),
    focus_areas: Optional[str] = Form(None, description="Comma-separated focus areas"),
    api_key: str = Form(..., description="Gemini API key")
):
    """
    Generate interview questions from uploaded resume and job description.
    
    Args:
        resume: Resume file (PDF, DOCX, or TXT)
        job_description: Text description of the job (optional if job_description_file provided)
        job_description_file: Job description file (PDF or DOCX - optional if job_description provided)
        round_type: Type of interview (technical, behavioral, etc.)
        difficulty: Difficulty level of questions
        num_questions: How many questions to generate
        focus_areas: Optional comma-separated list of focus areas
        
    Returns:
        QuestionGenerationResponse with generated questions
    """
    try:
        # Validate that at least one job description source is provided
        if not job_description and not job_description_file:
            raise HTTPException(
                status_code=400,
                detail="Either job_description text or job_description_file must be provided"
            )
        
        # Validate resume file type
        supported_formats = ['.pdf', '.docx', '.txt']
        file_lower = resume.filename.lower()
        if not any(file_lower.endswith(fmt) for fmt in supported_formats):
            raise HTTPException(
                status_code=400,
                detail="Only PDF, DOCX, and TXT files are supported for resumes"
            )
        
        # Read and parse resume
        logger.info(f"Processing resume: {resume.filename}")
        resume_bytes = await resume.read()
        
        try:
            resume_data = resume_parser.parse_resume_bytes(resume_bytes, resume.filename)
        except ResumeParserError as e:
            raise HTTPException(status_code=400, detail=f"Resume parsing error: {str(e)}")
        
        # Process job description - either from text or file
        if job_description_file and job_description_file.filename:
            logger.info(f"Processing job description file: {job_description_file.filename}")
            
            # Validate JD file type - only PDF and DOCX allowed
            jd_file_lower = job_description_file.filename.lower()
            if not (jd_file_lower.endswith('.pdf') or jd_file_lower.endswith('.docx')):
                raise HTTPException(
                    status_code=400,
                    detail="Only PDF and DOCX files are supported for job description"
                )
            
            jd_bytes = await job_description_file.read()
            
            try:
                job_description = resume_parser.extract_text_from_file(jd_bytes, job_description_file.filename)
                logger.info(f"Successfully extracted job description from file ({len(job_description)} characters)")
            except Exception as e:
                logger.error(f"Error extracting job description: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to extract text from job description file: {str(e)}"
                )
        
        # Parse focus areas if provided
        focus_list = None
        if focus_areas:
            focus_list = [area.strip() for area in focus_areas.split(',')]
        
        # Generate questions
        logger.info(f"Generating {num_questions} {round_type} questions")
        
        try:
            # Create question agent with provided API key
            question_agent = InterviewQuestionAgent(api_key=api_key)
            
            response = question_agent.generate_questions(
                resume_text=resume_data.raw_text,
                job_description=job_description,
                round_type=round_type,
                difficulty=difficulty,
                num_questions=num_questions,
                focus_areas=focus_list
            )
        except InterviewAgentError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Question generation error: {str(e)}"
            )
        
        logger.info(f"Successfully generated {response.total_questions} questions")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/api/v1/generate-questions-json", response_model=QuestionGenerationResponse)
async def generate_questions_from_json(
    request: QuestionGenerationRequest,
    api_key: str = Form(..., description="Gemini API key")
):
    """
    Generate interview questions from JSON request.
    
    Args:
        request: QuestionGenerationRequest object
        
    Returns:
        QuestionGenerationResponse with generated questions
    """
    try:
        logger.info(
            f"Generating {request.num_questions} {request.round_type} questions "
            f"at {request.difficulty} level"
        )
        
        # Create question agent with provided API key
        question_agent = InterviewQuestionAgent(api_key=api_key)
        
        response = question_agent.generate_from_request(request)
        
        logger.info(f"Successfully generated {response.total_questions} questions")
        return response
        
    except InterviewAgentError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Question generation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/api/v1/parse-resume")
async def parse_resume_endpoint(resume: UploadFile = File(...)):
    """
    Parse a resume and return extracted information.
    
    Args:
        resume: Resume file (PDF, DOCX, or TXT)
        
    Returns:
        Parsed resume data
    """
    try:
        supported_formats = ['.pdf', '.docx', '.txt']
        file_lower = resume.filename.lower()
        if not any(file_lower.endswith(fmt) for fmt in supported_formats):
            raise HTTPException(
                status_code=400,
                detail="Only PDF, DOCX, and TXT files are supported"
            )
        
        logger.info(f"Parsing resume: {resume.filename}")
        resume_bytes = await resume.read()
        
        resume_data = resume_parser.parse_resume_bytes(resume_bytes, resume.filename)
        
        return {
            "name": resume_data.name,
            "email": resume_data.email,
            "skills": resume_data.skills,
            "text_preview": resume_data.raw_text[:500] + "..."
        }
        
    except ResumeParserError as e:
        raise HTTPException(status_code=400, detail=f"Resume parsing error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/error", response_class=HTMLResponse)
async def error_page(request: Request, message: str = "An unexpected error occurred"):
    """Serve error page."""
    return templates.TemplateResponse(
        "error.html", 
        {
            "request": request, 
            "error_message": message,
            "error_code": "UI_ERROR"
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Global exception: {str(exc)}")
    
    # Check if request is for HTML (web interface) or JSON (API)
    accept_header = request.headers.get("accept", "")
    if "text/html" in accept_header:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": "Something went wrong. Please try again.",
                "error_code": f"ERROR_{exc.__class__.__name__.upper()}"
            },
            status_code=500
        )
    else:
        # Return JSON for API requests
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred"}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
