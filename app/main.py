from app.model import QuestionGenerationRequest, QuestionGenerationResponse
from fastapi import FastAPI, HTTPException
import os
import genai

app = FastAPI()

@app.post("/api/v1/generate-questions", response_model=QuestionGenerationResponse)
async def generate_questions(request: QuestionGenerationRequest):
    try:
        # Comment out the environment variable
        # api_key = os.getenv("GEMINI_API_KEY")
        
        # Use the API key from the request
        genai.configure(api_key=request.api_key)
        
        # Rest of the existing code remains the same
        # ...existing code...
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))