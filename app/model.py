from pydantic import BaseModel

class QuestionGenerationRequest(BaseModel):
    topic: str
    difficulty_level: str
    num_questions: int
    api_key: str  # Add this line for the Gemini API key