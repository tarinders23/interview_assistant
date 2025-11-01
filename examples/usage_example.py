"""Example usage of the Interview Assistant."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent import InterviewQuestionAgent
from src.parsers import ResumeParser
from src.models import RoundType, DifficultyLevel


def example_with_pdf():
    """Example: Generate questions from a PDF resume."""
    print("=" * 80)
    print("Example 1: Generating questions from PDF resume")
    print("=" * 80)
    
    # Parse resume
    parser = ResumeParser()
    resume_data = parser.parse_pdf("examples/sample_resume.pdf")
    
    print(f"\nResume parsed successfully!")
    print(f"Name: {resume_data.name}")
    print(f"Email: {resume_data.email}")
    print(f"Skills found: {', '.join(resume_data.skills[:5])}...")
    
    # Job description
    job_description = """
    Senior Python Developer
    
    We are looking for an experienced Python developer to join our team.
    
    Requirements:
    - 5+ years of Python development experience
    - Strong knowledge of Django or Flask
    - Experience with RESTful APIs
    - Familiarity with AWS cloud services
    - Knowledge of PostgreSQL and Redis
    - Experience with Docker and CI/CD
    
    Responsibilities:
    - Design and implement scalable backend services
    - Write clean, maintainable code
    - Collaborate with cross-functional teams
    - Mentor junior developers
    """
    
    # Generate questions
    agent = InterviewQuestionAgent()
    response = agent.generate_questions(
        resume_text=resume_data.raw_text,
        job_description=job_description,
        round_type=RoundType.TECHNICAL,
        difficulty=DifficultyLevel.INTERMEDIATE,
        num_questions=5
    )
    
    print(f"\n\nGenerated {response.total_questions} questions:\n")
    
    for i, question in enumerate(response.questions, 1):
        print(f"\nQuestion {i}:")
        print(f"  Category: {question.category}")
        print(f"  Difficulty: {question.difficulty}")
        print(f"  Question: {question.question}")
        if question.expected_topics:
            print(f"  Expected topics: {', '.join(question.expected_topics)}")
        if question.follow_up_questions:
            print(f"  Follow-ups:")
            for fq in question.follow_up_questions:
                print(f"    - {fq}")


def example_with_text():
    """Example: Generate questions from text (no PDF)."""
    print("\n\n" + "=" * 80)
    print("Example 2: Generating behavioral interview questions")
    print("=" * 80)
    
    resume_text = """
    John Doe
    Senior Software Engineer
    
    Experience:
    - Lead Developer at Tech Corp (2020-Present)
      Led a team of 5 developers building microservices
      Improved system performance by 40%
    
    - Software Engineer at StartupXYZ (2018-2020)
      Developed RESTful APIs using Python and Django
      Implemented CI/CD pipelines
    
    Skills: Python, Django, AWS, Docker, PostgreSQL, Redis, React
    
    Education:
    BS Computer Science, University of Technology
    """
    
    job_description = """
    Senior Backend Engineer
    
    We need a senior engineer who can lead technical projects and mentor junior team members.
    Must have strong communication skills and experience working in agile teams.
    """
    
    agent = InterviewQuestionAgent()
    response = agent.generate_questions(
        resume_text=resume_text,
        job_description=job_description,
        round_type=RoundType.BEHAVIORAL,
        difficulty=DifficultyLevel.INTERMEDIATE,
        num_questions=5
    )
    
    print(f"\nGenerated {response.total_questions} behavioral questions:\n")
    
    for i, question in enumerate(response.questions, 1):
        print(f"\nQuestion {i}:")
        print(f"  Category: {question.category}")
        print(f"  Question: {question.question}")
        if question.context:
            print(f"  Evaluates: {question.context}")


def example_system_design():
    """Example: Generate system design questions."""
    print("\n\n" + "=" * 80)
    print("Example 3: Generating system design questions")
    print("=" * 80)
    
    resume_text = """
    Jane Smith
    Staff Software Engineer
    
    10+ years of experience building distributed systems at scale.
    
    Experience:
    - Staff Engineer at MegaCorp (2018-Present)
      Designed and implemented microservices architecture serving 10M+ users
      Led migration from monolith to microservices
      Expertise in AWS, Kubernetes, and distributed databases
    
    - Senior Engineer at CloudTech (2015-2018)
      Built real-time data processing pipelines
      Implemented event-driven architecture using Kafka
    
    Skills: System Design, Microservices, AWS, Kubernetes, PostgreSQL, 
            Redis, Kafka, MongoDB, Elasticsearch
    """
    
    job_description = """
    Principal Engineer
    
    Looking for a senior architect to design and implement large-scale distributed systems.
    Must have experience with high-traffic systems, scalability, and reliability.
    """
    
    agent = InterviewQuestionAgent()
    response = agent.generate_questions(
        resume_text=resume_text,
        job_description=job_description,
        round_type=RoundType.SYSTEM_DESIGN,
        difficulty=DifficultyLevel.ADVANCED,
        num_questions=3
    )
    
    print(f"\nGenerated {response.total_questions} system design questions:\n")
    
    for i, question in enumerate(response.questions, 1):
        print(f"\nQuestion {i}:")
        print(f"  Category: {question.category}")
        print(f"  Question: {question.question}")
        if question.expected_topics:
            print(f"  Topics to discuss: {', '.join(question.expected_topics)}")


if __name__ == "__main__":
    try:
        # Run examples that don't require PDF
        example_with_text()
        example_system_design()
        
        # Uncomment to run PDF example if you have a sample resume
        # example_with_pdf()
        
        print("\n" + "=" * 80)
        print("Examples completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nError running examples: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set OPENAI_API_KEY in your .env file")
        print("2. Installed all dependencies: pip install -r requirements.txt")
