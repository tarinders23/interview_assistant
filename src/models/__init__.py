"""Data models for interview assistant using Pydantic."""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum


class RoundType(str, Enum):
    """Interview round types."""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SYSTEM_DESIGN = "system_design"
    CODING = "coding"
    DOMAIN_SPECIFIC = "domain_specific"


class DifficultyLevel(str, Enum):
    """Question difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ResumeData(BaseModel):
    """Parsed resume data."""
    raw_text: str
    name: Optional[str] = None
    email: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    experience_years: Optional[int] = None
    education: List[str] = Field(default_factory=list)
    work_history: List[str] = Field(default_factory=list)


class JobDescription(BaseModel):
    """Job description model."""
    title: str
    description: str
    required_skills: List[str] = Field(default_factory=list)
    experience_level: Optional[str] = None
    company: Optional[str] = None


class InterviewQuestion(BaseModel):
    """Generated interview question."""
    question: str
    category: str
    difficulty: DifficultyLevel
    context: Optional[str] = None
    follow_up_questions: List[str] = Field(default_factory=list)
    expected_topics: List[str] = Field(default_factory=list)


class QuestionGenerationRequest(BaseModel):
    """Request model for question generation."""
    resume_text: str
    job_description: str
    round_type: RoundType
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    num_questions: int = Field(default=10, ge=1, le=50)
    focus_areas: Optional[List[str]] = None


class QuestionGenerationResponse(BaseModel):
    """Response model with generated questions."""
    questions: List[InterviewQuestion]
    total_questions: int
    round_type: RoundType
    difficulty: DifficultyLevel
    metadata: Optional[dict] = None
