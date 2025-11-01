#!/usr/bin/env python3
"""
Simple test script to verify Gemini integration works.
Run this script with a valid GEMINI_API_KEY in your .env file.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.agent import InterviewQuestionAgent
from src.models import RoundType, DifficultyLevel
from src.config import settings


def test_gemini_integration():
    """Test Gemini API integration with sample data."""
    
    # Check if we have a real API key (not the demo key)
    if settings.gemini_api_key == "demo_api_key_replace_with_real_key":
        print("❌ Please set a real GEMINI_API_KEY in your .env file")
        print("   Visit https://aistudio.google.com/app/apikey to get your API key")
        return False
    
    print("🚀 Testing Gemini integration...")
    print(f"   Model: {settings.model_name}")
    print(f"   Temperature: {settings.temperature}")
    
    # Sample data
    sample_resume = """
    John Doe
    Senior Python Developer
    
    Experience:
    - 5 years of Python development
    - Expert in Django, FastAPI, and Flask
    - Experience with PostgreSQL and Redis
    - Cloud deployment on AWS
    - Test-driven development practices
    
    Skills:
    Python, Django, FastAPI, PostgreSQL, Redis, Docker, AWS, Git
    """
    
    sample_job_description = """
    Senior Backend Developer Position
    
    We are looking for a Senior Backend Developer with strong Python experience.
    The ideal candidate will have:
    - 4+ years of Python development experience
    - Experience with Django or FastAPI
    - Database design and optimization skills
    - Cloud deployment experience
    - Strong problem-solving abilities
    """
    
    try:
        # Initialize agent
        agent = InterviewQuestionAgent()
        print("✅ Agent initialized successfully")
        
        # Generate questions
        print("🤖 Generating questions...")
        response = agent.generate_questions(
            resume_text=sample_resume,
            job_description=sample_job_description,
            round_type=RoundType.TECHNICAL,
            difficulty=DifficultyLevel.INTERMEDIATE,
            num_questions=3
        )
        
        print(f"✅ Generated {response.total_questions} questions")
        print(f"   Round Type: {response.round_type}")
        print(f"   Difficulty: {response.difficulty}")
        
        # Display questions
        print("\n📝 Generated Questions:")
        print("=" * 50)
        for i, question in enumerate(response.questions, 1):
            print(f"\n{i}. {question.question}")
            print(f"   Category: {question.category}")
            if question.expected_topics:
                print(f"   Expected Topics: {', '.join(question.expected_topics)}")
            if question.follow_up_questions:
                print(f"   Follow-ups: {len(question.follow_up_questions)} questions")
        
        print("\n🎉 Gemini integration test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_gemini_integration()
    sys.exit(0 if success else 1)
