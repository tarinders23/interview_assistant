"""Gemini AI agent for generating interview questions."""

import json
import logging
import os
from typing import List, Optional

from google import genai
from google.genai import types
from google.genai import errors

from ..models import (
    InterviewQuestion,
    QuestionGenerationRequest,
    QuestionGenerationResponse, 
    RoundType,
    DifficultyLevel
)
from ..prompts.templates import PROMPT_TEMPLATES
from ..config import settings


logger = logging.getLogger(__name__)


class InterviewQuestionAgent:
    """AI agent for generating interview questions using Google Gemini."""
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        """
        Initialize the interview question agent.
        
        Args:
            model_name: Gemini model to use (defaults to config)
            temperature: Temperature for generation (defaults to config)
            max_tokens: Max tokens to generate (defaults to config)
        """
        self.model_name = model_name or settings.model_name
        self.temperature = temperature or settings.temperature
        self.max_tokens = max_tokens or settings.max_tokens
        
        # Set API key as environment variable if not already set
        if not os.getenv('GEMINI_API_KEY'):
            os.environ['GEMINI_API_KEY'] = settings.gemini_api_key
        
        # Initialize the Gemini client
        self.client = genai.Client(api_key=settings.gemini_api_key)

        logger.info(f"Initialized InterviewQuestionAgent with model: {self.model_name}")
    
    def generate_questions(
        self,
        resume_text: str,
        job_description: str,
        round_type: RoundType,
        difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE,
        num_questions: int = 10,
        focus_areas: Optional[List[str]] = None
    ) -> QuestionGenerationResponse:
        """
        Generate interview questions based on resume and job description.
        
        Args:
            resume_text: Parsed resume text
            job_description: Job description text
            round_type: Type of interview round
            difficulty: Difficulty level of questions
            num_questions: Number of questions to generate
            focus_areas: Optional specific areas to focus on
            
        Returns:
            QuestionGenerationResponse with generated questions
        """
        try:
            logger.info(
                f"Generating {num_questions} {round_type} questions "
                f"at {difficulty} level"  
            )
            
            # Get the appropriate prompt template
            prompt_template = PROMPT_TEMPLATES.get(round_type.value)
            if not prompt_template:
                raise ValueError(f"No prompt template found for round type: {round_type}")
            
            # Prepare focus areas text if provided
            focus_text = ""
            if focus_areas:
                focus_text = f"\nFOCUS AREAS: {', '.join(focus_areas)}"
            
            # Prepare input variables for the prompt
            input_vars = {
                "resume": resume_text[:4000],  # Limit resume text to avoid token limits
                "job_description": job_description[:2000], 
                "difficulty": difficulty.value,
                "num_questions": num_questions,
            }
            
            # Add optional variables
            if "focus_areas" in prompt_template.input_variables:
                input_vars["focus_areas"] = focus_text
            if "domain" in prompt_template.input_variables and focus_areas:
                input_vars["domain"] = ", ".join(focus_areas)
            
            # Format the prompt with variables
            formatted_prompt = prompt_template.format(**input_vars)
            
            # Generate questions using Gemini with JSON output
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=formatted_prompt,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                    response_mime_type="application/json"
                    # Note: response_schema is optional and can cause issues
                    # The prompt template already instructs for proper JSON format
                )
            )
            
            # Parse the response
            questions = self._parse_questions(response.text, difficulty)
            
            logger.info(f"Successfully generated {len(questions)} questions")
            
            return QuestionGenerationResponse(
                questions=questions,
                total_questions=len(questions),
                round_type=round_type,
                difficulty=difficulty,
                metadata={
                    "model": self.model_name,
                    "temperature": self.temperature
                }
            )
            
        except errors.APIError as e:
            logger.error(f"Gemini API error: {e.code} - {e.message}")
            raise InterviewAgentError(f"API request failed: {e.message}")
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            raise InterviewAgentError(f"Question generation failed: {str(e)}")
    
    def _parse_questions(
        self,
        llm_response: str,
        difficulty: DifficultyLevel
    ) -> List[InterviewQuestion]:
        """
        Parse the LLM response into InterviewQuestion objects.
        
        Args:
            llm_response: Raw response from the LLM
            difficulty: Difficulty level for the questions
            
        Returns:
            List of InterviewQuestion objects
        """
        logger.info(f"DEBUG: RESPONSE: {llm_response}")
        try:
            # Handle None or empty response
            if not llm_response:
                logger.error("Received empty or None response from Gemini API")
                return [
                    InterviewQuestion(
                        question="Unable to generate questions - API key may be invalid or quota exceeded",
                        category="Error",
                        difficulty=difficulty,
                        context="API error - check your Gemini API key"
                    )
                ]
            
            # Extract JSON from response (handle markdown code blocks)
            response_text = llm_response.strip()
            
            # Remove markdown code block markers if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            elif response_text.startswith("```"):
                response_text = response_text[3:]
            
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            questions_data = json.loads(response_text)
            
            # Convert to InterviewQuestion objects
            questions = []
            for q_data in questions_data:
                question = InterviewQuestion(
                    question=q_data.get("question", ""),
                    category=q_data.get("category", "General"),
                    difficulty=difficulty,
                    context=q_data.get("context"),
                    follow_up_questions=q_data.get("follow_up_questions", []),
                    expected_topics=q_data.get("expected_topics", [])
                )
                questions.append(question)
            
            return questions
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.debug(f"Raw response: {llm_response}")
            
            # Try to fix common JSON issues
            try:
                # Attempt to find and extract just the JSON array part
                response_text = llm_response.strip()
                
                # Look for JSON array start
                start_idx = response_text.find('[')
                if start_idx != -1:
                    # Find the matching closing bracket (simple approach)
                    bracket_count = 0
                    end_idx = start_idx
                    for i, char in enumerate(response_text[start_idx:], start_idx):
                        if char == '[':
                            bracket_count += 1
                        elif char == ']':
                            bracket_count -= 1
                            if bracket_count == 0:
                                end_idx = i + 1
                                break
                    
                    if end_idx > start_idx:
                        json_text = response_text[start_idx:end_idx]
                        questions_data = json.loads(json_text)
                        
                        # Convert to InterviewQuestion objects
                        questions = []
                        for q_data in questions_data:
                            question = InterviewQuestion(
                                question=q_data.get("question", ""),
                                category=q_data.get("category", "General"),
                                difficulty=difficulty,
                                context=q_data.get("context"),
                                follow_up_questions=q_data.get("follow_up_questions", []),
                                expected_topics=q_data.get("expected_topics", [])
                            )
                            questions.append(question)
                        
                        return questions
                        
            except Exception as retry_e:
                logger.error(f"JSON recovery attempt also failed: {str(retry_e)}")
            
            # Final fallback: create a single question with the raw response
            response_preview = (llm_response or "No response")[:500]
            return [
                InterviewQuestion(
                    question=response_preview,
                    category="General", 
                    difficulty=difficulty,
                    context="Raw response - parsing failed"
                )
            ]
        except Exception as e:
            logger.error(f"Error parsing questions: {str(e)}")
            raise
    
    def generate_from_request(
        self,
        request: QuestionGenerationRequest
    ) -> QuestionGenerationResponse:
        """
        Generate questions from a QuestionGenerationRequest object.
        
        Args:
            request: Request object with all parameters
            
        Returns:
            QuestionGenerationResponse with generated questions
        """
        return self.generate_questions(
            resume_text=request.resume_text,
            job_description=request.job_description,
            round_type=request.round_type,
            difficulty=request.difficulty,
            num_questions=request.num_questions,
            focus_areas=request.focus_areas
        )


class InterviewAgentError(Exception):
    """Custom exception for interview agent errors."""
    pass
