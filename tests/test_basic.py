"""Basic tests for the Interview Assistant."""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path

# Note: These are basic tests. Full test suite would require mocking OpenAI API


def test_imports():
    """Test that all modules can be imported."""
    from src.agent import InterviewQuestionAgent
    from src.parsers import ResumeParser
    from src.models import RoundType, DifficultyLevel
    from src.config import settings
    
    assert InterviewQuestionAgent is not None
    assert ResumeParser is not None
    assert RoundType is not None
    assert DifficultyLevel is not None


def test_round_types():
    """Test that all round types are defined."""
    from src.models import RoundType
    
    assert RoundType.TECHNICAL.value == "technical"
    assert RoundType.BEHAVIORAL.value == "behavioral"
    assert RoundType.SYSTEM_DESIGN.value == "system_design"
    assert RoundType.CODING.value == "coding"
    assert RoundType.DOMAIN_SPECIFIC.value == "domain_specific"


def test_difficulty_levels():
    """Test that all difficulty levels are defined."""
    from src.models import DifficultyLevel
    
    assert DifficultyLevel.BEGINNER.value == "beginner"
    assert DifficultyLevel.INTERMEDIATE.value == "intermediate"
    assert DifficultyLevel.ADVANCED.value == "advanced"
    assert DifficultyLevel.EXPERT.value == "expert"


def test_resume_data_model():
    """Test ResumeData model."""
    from src.models import ResumeData
    
    resume = ResumeData(
        raw_text="Test resume text",
        name="John Doe",
        email="john@example.com",
        skills=["Python", "Django"]
    )
    
    assert resume.raw_text == "Test resume text"
    assert resume.name == "John Doe"
    assert resume.email == "john@example.com"
    assert len(resume.skills) == 2


def test_interview_question_model():
    """Test InterviewQuestion model."""
    from src.models import InterviewQuestion, DifficultyLevel
    
    question = InterviewQuestion(
        question="What is a decorator in Python?",
        category="Python",
        difficulty=DifficultyLevel.INTERMEDIATE,
        expected_topics=["decorators", "functions", "syntax"]
    )
    
    assert question.question == "What is a decorator in Python?"
    assert question.category == "Python"
    assert question.difficulty == DifficultyLevel.INTERMEDIATE
    assert len(question.expected_topics) == 3


def test_question_generation_request():
    """Test QuestionGenerationRequest validation."""
    from src.models import QuestionGenerationRequest, RoundType, DifficultyLevel
    
    request = QuestionGenerationRequest(
        resume_text="Resume text",
        job_description="Job description",
        round_type=RoundType.TECHNICAL,
        difficulty=DifficultyLevel.INTERMEDIATE,
        num_questions=10
    )
    
    assert request.num_questions == 10
    assert request.round_type == RoundType.TECHNICAL


def test_question_generation_request_validation():
    """Test that num_questions validation works."""
    from src.models import QuestionGenerationRequest, RoundType
    import pydantic
    
    # Test valid range
    request = QuestionGenerationRequest(
        resume_text="Resume",
        job_description="JD",
        round_type=RoundType.TECHNICAL,
        num_questions=25
    )
    assert request.num_questions == 25
    
    # Test invalid range (should raise validation error)
    with pytest.raises(pydantic.ValidationError):
        QuestionGenerationRequest(
            resume_text="Resume",
            job_description="JD",
            round_type=RoundType.TECHNICAL,
            num_questions=100  # Over limit
        )


def test_resume_parser_initialization():
    """Test ResumeParser initialization."""
    from src.parsers import ResumeParser
    
    parser = ResumeParser()
    assert parser is not None
    assert hasattr(parser, 'parse_pdf')
    assert hasattr(parser, 'parse_pdf_bytes')


def test_prompt_templates_exist():
    """Test that all prompt templates are defined."""
    from src.prompts.templates import PROMPT_TEMPLATES
    
    assert "technical" in PROMPT_TEMPLATES
    assert "behavioral" in PROMPT_TEMPLATES
    assert "system_design" in PROMPT_TEMPLATES
    assert "coding" in PROMPT_TEMPLATES
    assert "domain_specific" in PROMPT_TEMPLATES


def test_api_app_creation():
    """Test that FastAPI app can be created."""
    from src.api.main import app
    
    assert app is not None
    assert app.title == "Interview Assistant API"


# Integration test (requires mocking or real API key)
@pytest.mark.skip(reason="Requires OpenAI API key")
def test_question_generation_integration():
    """Integration test for question generation."""
    from src.agent import InterviewQuestionAgent
    from src.models import RoundType, DifficultyLevel
    
    agent = InterviewQuestionAgent()
    response = agent.generate_questions(
        resume_text="Python developer with 5 years experience",
        job_description="Senior Python Developer position",
        round_type=RoundType.TECHNICAL,
        difficulty=DifficultyLevel.INTERMEDIATE,
        num_questions=5
    )
    
    assert response.total_questions == 5
    assert len(response.questions) == 5
    assert response.round_type == RoundType.TECHNICAL


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
