# 🎯 Interview Assistant - Installation & Usage Guide

## Quick Installation (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- langchain & langchain-openai (AI framework)
- openai (GPT-4 access)
- pdfplumber (PDF parsing)
- fastapi & uvicorn (Web API)
- pydantic (Data validation)
- python-dotenv (Configuration)

### Step 2: Configure API Key

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### Step 3: Verify Setup

```bash
python verify_setup.py
```

You should see all green checkmarks ✅!

## Usage Examples

### Example 1: Python API (Recommended)

```python
from src.agent import InterviewQuestionAgent
from src.models import RoundType, DifficultyLevel

# Initialize agent
agent = InterviewQuestionAgent()

# Generate technical questions
response = agent.generate_questions(
    resume_text="""
    Senior Python Developer
    5 years experience with Django, FastAPI, PostgreSQL
    Built microservices handling 10M requests/day
    """,
    job_description="""
    Senior Backend Engineer
    Required: Python, Django/FastAPI, AWS, Docker
    Must have experience with high-traffic systems
    """,
    round_type=RoundType.TECHNICAL,
    difficulty=DifficultyLevel.INTERMEDIATE,
    num_questions=10
)

# Display questions
for i, q in enumerate(response.questions, 1):
    print(f"\nQ{i}: {q.question}")
    print(f"Category: {q.category}")
    print(f"Expected topics: {', '.join(q.expected_topics)}")
```

### Example 2: Command Line Interface

```bash
# Generate technical questions
python cli.py resume.pdf "Senior Python Developer role" \
  --round-type technical \
  --difficulty intermediate \
  --num-questions 10 \
  --output questions.txt

# Generate behavioral questions
python cli.py resume.pdf job_description.txt \
  --round-type behavioral \
  --num-questions 8

# Focus on specific technologies
python cli.py resume.pdf job.txt \
  --round-type technical \
  --focus-areas "Python,AWS,Kubernetes" \
  --output questions.json \
  --format json
```

### Example 3: REST API

**Start the server:**
```bash
python run_api.py
```

**Generate questions:**
```bash
curl -X POST "http://localhost:8000/api/v1/generate-questions" \
  -H "accept: application/json" \
  -F "resume=@resume.pdf" \
  -F "job_description=Senior Python Developer position..." \
  -F "round_type=technical" \
  -F "difficulty=intermediate" \
  -F "num_questions=10"
```

**Interactive API docs:**
Open http://localhost:8000/docs in your browser

## Interview Round Types

### 1. Technical (`technical`)
Tests coding knowledge and technical skills
```python
round_type=RoundType.TECHNICAL
```
Example questions:
- "Explain the difference between `@staticmethod` and `@classmethod` in Python"
- "How would you optimize a slow database query?"

### 2. Behavioral (`behavioral`)
Assesses soft skills and cultural fit using STAR method
```python
round_type=RoundType.BEHAVIORAL
```
Example questions:
- "Tell me about a time when you had to handle a difficult stakeholder"
- "Describe a situation where you had to learn a new technology quickly"

### 3. System Design (`system_design`)
Evaluates architectural thinking and scalability knowledge
```python
round_type=RoundType.SYSTEM_DESIGN
```
Example questions:
- "Design a URL shortening service like bit.ly"
- "How would you design a rate limiter for an API?"

### 4. Coding (`coding`)
Algorithm and data structure problems
```python
round_type=RoundType.CODING
```
Example questions:
- "Write a function to find the longest substring without repeating characters"
- "Implement a LRU cache with O(1) operations"

### 5. Domain Specific (`domain_specific`)
Specialized questions for specific domains
```python
round_type=RoundType.DOMAIN_SPECIFIC
focus_areas=["Machine Learning", "Data Science"]
```

## Difficulty Levels

| Level | Experience | Use For |
|-------|-----------|---------|
| `beginner` | 0-2 years | Junior roles, interns |
| `intermediate` | 2-5 years | Mid-level positions |
| `advanced` | 5-8 years | Senior engineers |
| `expert` | 8+ years | Staff/Principal roles |

## Advanced Usage

### With PDF Resume

```python
from src.parsers import ResumeParser

# Parse PDF resume
parser = ResumeParser()
resume_data = parser.parse_pdf("candidate_resume.pdf")

print(f"Candidate: {resume_data.name}")
print(f"Email: {resume_data.email}")
print(f"Skills: {resume_data.skills}")

# Generate questions
agent = InterviewQuestionAgent()
response = agent.generate_questions(
    resume_text=resume_data.raw_text,
    job_description="...",
    round_type=RoundType.TECHNICAL,
    num_questions=10
)
```

### Customize Model Settings

```python
# Use different model or settings
agent = InterviewQuestionAgent(
    model_name="gpt-4-turbo",
    temperature=0.8,  # More creative
    max_tokens=3000
)
```

### Multiple Interview Rounds

```python
# Generate questions for all interview stages
rounds = [
    (RoundType.TECHNICAL, 15, DifficultyLevel.INTERMEDIATE),
    (RoundType.BEHAVIORAL, 8, DifficultyLevel.INTERMEDIATE),
    (RoundType.SYSTEM_DESIGN, 5, DifficultyLevel.ADVANCED),
]

all_questions = {}
for round_type, num, difficulty in rounds:
    response = agent.generate_questions(
        resume_text=resume_text,
        job_description=job_description,
        round_type=round_type,
        difficulty=difficulty,
        num_questions=num
    )
    all_questions[round_type.value] = response.questions
```

## Tips for Best Results

### ✅ DO:
- Provide detailed job descriptions
- Use appropriate difficulty levels
- Specify focus areas for targeted questions
- Include years of experience in job description
- Mention specific technologies required

### ❌ DON'T:
- Use vague job descriptions
- Generate too many questions at once (max 20)
- Skip the focus areas for niche roles
- Use mismatched difficulty levels

## Sample Output

```json
{
  "questions": [
    {
      "question": "Can you explain the difference between Django's ORM and SQLAlchemy?",
      "category": "Python/Django",
      "difficulty": "intermediate",
      "expected_topics": [
        "ORM concepts",
        "Django model layer",
        "SQLAlchemy flexibility",
        "Use cases for each"
      ],
      "follow_up_questions": [
        "When would you choose one over the other?",
        "How do you handle complex queries in Django ORM?"
      ]
    }
  ],
  "total_questions": 10,
  "round_type": "technical",
  "difficulty": "intermediate"
}
```

## Troubleshooting

### Problem: "OpenAI API key not found"
**Solution:** 
```bash
# Make sure .env file exists
cp .env.example .env

# Add your API key
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
```

### Problem: "Failed to parse PDF"
**Solution:**
- Ensure PDF is not password-protected
- Check that PDF contains actual text (not scanned image)
- Try: `python -c "import pdfplumber; print(pdfplumber.open('resume.pdf').pages[0].extract_text())"`

### Problem: "Rate limit exceeded"
**Solution:**
- Wait a minute and retry
- Reduce num_questions
- Check OpenAI API usage limits

### Problem: Import errors
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

## Performance Tips

### 1. Cache Common Job Descriptions
```python
# Cache job descriptions you use frequently
common_jds = {
    "senior_python": "...",
    "data_scientist": "...",
}
```

### 2. Batch Processing
```python
# Process multiple candidates
for resume_file in resume_files:
    resume_data = parser.parse_pdf(resume_file)
    questions = agent.generate_questions(...)
    # Save or process questions
```

### 3. Parallel Processing
```python
from concurrent.futures import ThreadPoolExecutor

def generate_for_candidate(resume_file):
    resume_data = parser.parse_pdf(resume_file)
    return agent.generate_questions(...)

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(generate_for_candidate, resume_files))
```

## Integration Examples

### With ATS (Applicant Tracking System)
```python
# Webhook receiver
@app.post("/ats/candidate")
async def handle_new_candidate(candidate_data: dict):
    # Parse resume
    resume = parser.parse_pdf_bytes(candidate_data['resume_bytes'])
    
    # Generate questions
    questions = agent.generate_questions(
        resume_text=resume.raw_text,
        job_description=candidate_data['job_description'],
        round_type=RoundType.TECHNICAL,
        num_questions=10
    )
    
    # Send to ATS
    ats_client.update_candidate(candidate_data['id'], questions)
```

### With Email Service
```python
import smtplib
from email.mime.text import MIMEText

def email_questions(to_email, questions):
    body = "\n\n".join([
        f"Q{i}: {q.question}" 
        for i, q in enumerate(questions, 1)
    ])
    
    msg = MIMEText(body)
    msg['Subject'] = 'Interview Questions'
    msg['To'] = to_email
    
    # Send email
    # ... smtp code ...
```

## API Reference

See the interactive docs at http://localhost:8000/docs when running the server.

### Endpoints:

1. **POST /api/v1/generate-questions** - Generate from uploaded PDF
2. **POST /api/v1/generate-questions-json** - Generate from JSON
3. **POST /api/v1/parse-resume** - Parse resume only
4. **GET /health** - Health check

## Next Steps

1. ✅ Install and verify setup
2. ✅ Try the examples
3. ✅ Generate your first questions
4. Read [Architecture Documentation](docs/architecture.md)
5. Customize prompts in `src/prompts/templates.py`
6. Integrate with your workflow
7. Deploy to production

## Getting Help

- 📖 Read the [README.md](README.md)
- 🏗️ Check [Architecture docs](docs/architecture.md)
- 🚀 Try [examples/usage_example.py](examples/usage_example.py)
- 📝 Review sample job descriptions in [examples/](examples/)

## Production Deployment

### Docker
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run_api.py"]
```

### Environment Variables for Production
```env
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4-turbo
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
LOG_LEVEL=INFO
```

Happy Interviewing! 🎯
