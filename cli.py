#!/usr/bin/env python
"""Command-line interface for Interview Assistant."""

import sys
import os
import argparse
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent import InterviewQuestionAgent
from src.parsers import ResumeParser
from src.models import RoundType, DifficultyLevel


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Interview Assistant - Generate AI-powered interview questions"
    )
    
    parser.add_argument(
        "resume",
        help="Path to resume PDF file or '-' to use text from job description only"
    )
    
    parser.add_argument(
        "job_description",
        help="Path to job description text file or job description text"
    )
    
    parser.add_argument(
        "--round-type",
        "-r",
        choices=["technical", "behavioral", "system_design", "coding", "domain_specific"],
        default="technical",
        help="Type of interview round (default: technical)"
    )
    
    parser.add_argument(
        "--difficulty",
        "-d",
        choices=["beginner", "intermediate", "advanced", "expert"],
        default="intermediate",
        help="Question difficulty level (default: intermediate)"
    )
    
    parser.add_argument(
        "--num-questions",
        "-n",
        type=int,
        default=10,
        help="Number of questions to generate (default: 10)"
    )
    
    parser.add_argument(
        "--focus-areas",
        "-f",
        help="Comma-separated focus areas (e.g., 'Python,AWS,Docker')"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: print to console)"
    )
    
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    args = parser.parse_args()
    
    try:
        # Parse resume
        if args.resume == "-":
            resume_text = "No resume provided"
        else:
            resume_path = Path(args.resume)
            if not resume_path.exists():
                print(f"Error: Resume file not found: {args.resume}")
                return 1
            
            print(f"Parsing resume: {args.resume}")
            parser_obj = ResumeParser()
            resume_data = parser_obj.parse_pdf(str(resume_path))
            resume_text = resume_data.raw_text
            print(f"✓ Resume parsed successfully")
            if resume_data.name:
                print(f"  Candidate: {resume_data.name}")
            if resume_data.skills:
                print(f"  Skills found: {len(resume_data.skills)}")
        
        # Read job description
        jd_path = Path(args.job_description)
        if jd_path.exists():
            job_description = jd_path.read_text()
        else:
            job_description = args.job_description
        
        # Parse focus areas
        focus_areas = None
        if args.focus_areas:
            focus_areas = [area.strip() for area in args.focus_areas.split(',')]
        
        # Generate questions
        print(f"\nGenerating {args.num_questions} {args.round_type} questions...")
        print(f"Difficulty: {args.difficulty}")
        
        agent = InterviewQuestionAgent()
        response = agent.generate_questions(
            resume_text=resume_text,
            job_description=job_description,
            round_type=RoundType(args.round_type),
            difficulty=DifficultyLevel(args.difficulty),
            num_questions=args.num_questions,
            focus_areas=focus_areas
        )
        
        print(f"✓ Generated {response.total_questions} questions\n")
        
        # Format output
        if args.format == "json":
            output = response.model_dump_json(indent=2)
        else:
            output = format_text_output(response)
        
        # Write or print output
        if args.output:
            Path(args.output).write_text(output)
            print(f"✓ Questions saved to: {args.output}")
        else:
            print(output)
        
        return 0
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        return 1


def format_text_output(response) -> str:
    """Format response as readable text."""
    lines = []
    lines.append("=" * 80)
    lines.append(f"INTERVIEW QUESTIONS - {response.round_type.value.upper()}")
    lines.append(f"Difficulty: {response.difficulty.value}")
    lines.append(f"Total Questions: {response.total_questions}")
    lines.append("=" * 80)
    
    for i, question in enumerate(response.questions, 1):
        lines.append(f"\nQuestion {i}")
        lines.append("-" * 80)
        lines.append(f"Category: {question.category}")
        lines.append(f"Difficulty: {question.difficulty.value}")
        lines.append(f"\n{question.question}")
        
        if question.context:
            lines.append(f"\nContext: {question.context}")
        
        if question.expected_topics:
            lines.append(f"\nExpected Topics:")
            for topic in question.expected_topics:
                lines.append(f"  • {topic}")
        
        if question.follow_up_questions:
            lines.append(f"\nFollow-up Questions:")
            for fq in question.follow_up_questions:
                lines.append(f"  • {fq}")
        
        lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
