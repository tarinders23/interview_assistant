# Quick Start Guide

Get up and running with Interview Assistant in 5 minutes!

## Prerequisites

- Python 3.10 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- pip (Python package installer)

## Step 1: Installation

Clone or download the project, then install dependencies:

```bash
cd interview_assistant
pip install -r requirements.txt
```

## Step 2: Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-api-key-here
MODEL_NAME=gpt-4-turbo
TEMPERATURE=0.7
MAX_TOKENS=2000
```

## Step 3: Test the Installation

Run a quick test:

```bash
python examples/usage_example.py
```

You should see interview questions being generated!

## Using the CLI

The CLI is the easiest way to generate questions:

```bash
python cli.py resume.pdf "job_description.txt" \
  --round-type technical \
  --difficulty intermediate \
  --num-questions 10 \
  --output questions.txt
```

### CLI Options:

- `resume`: Path to PDF resume (or use `-` for text-only)
- `job_description`: Path to job description file or text
- `--round-type`: technical, behavioral, system_design, coding, domain_specific
- `--difficulty`: beginner, intermediate, advanced, expert
- `--num-questions`: How many questions to generate (1-50)
- `--focus-areas`: Comma-separated focus areas (e.g., "Python,AWS,Docker")
- `--output`: Save to file (optional)
- `--format`: text or json

### Examples:

**Generate technical questions:**
```bash
python cli.py resume.pdf "Senior Python Developer position" \
  --round-type technical \
  --difficulty intermediate \
  --num-questions 15
```

**Generate behavioral questions:**
```bash
python cli.py resume.pdf "Team Lead role" \
  --round-type behavioral \
  --num-questions 10
```

**Focus on specific areas:**
```bash
python cli.py resume.pdf "job.txt" \
  --round-type technical \
  --focus-areas "Python,FastAPI,PostgreSQL" \
  --output technical_questions.json \
  --format json
```

## Using the REST API

### Start the API Server:

```bash
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`

Visit `http://localhost:8000/docs` for interactive API documentation.

### API Endpoints:

#### 1. Generate Questions (File Upload)

```bash
curl -X POST "http://localhost:8000/api/v1/generate-questions" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "resume=@resume.pdf" \
  -F "job_description=Senior Python Developer..." \
  -F "round_type=technical" \
  -F "difficulty=intermediate" \
  -F "num_questions=10"
```

#### 2. Generate Questions (JSON)

```bash
curl -X POST "http://localhost:8000/api/v1/generate-questions-json" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "John Doe, Software Engineer...",
    "job_description": "Senior Python Developer...",
    "round_type": "technical",
    "difficulty": "intermediate",
    "num_questions": 10
  }'
```

#### 3. Parse Resume Only

```bash
curl -X POST "http://localhost:8000/api/v1/parse-resume" \
  -F "resume=@resume.pdf"
```

## Using the Python API

Create a Python script:

```python
from src.agent import InterviewQuestionAgent
from src.parsers import ResumeParser
from src.models import RoundType, DifficultyLevel

# Parse resume
parser = ResumeParser()
resume_data = parser.parse_pdf("resume.pdf")

# Generate questions
agent = InterviewQuestionAgent()
response = agent.generate_questions(
    resume_text=resume_data.raw_text,
    job_description="Your job description here...",
    round_type=RoundType.TECHNICAL,
    difficulty=DifficultyLevel.INTERMEDIATE,
    num_questions=10
)

# Print questions
for i, question in enumerate(response.questions, 1):
    print(f"\nQ{i}: {question.question}")
    print(f"Category: {question.category}")
```

## Common Use Cases

### 1. Technical Screening

Generate questions to assess technical skills:

```python
response = agent.generate_questions(
    resume_text=resume_text,
    job_description=job_description,
    round_type=RoundType.TECHNICAL,
    difficulty=DifficultyLevel.INTERMEDIATE,
    num_questions=15,
    focus_areas=["Python", "Django", "PostgreSQL"]
)
```

### 2. Behavioral Interview

Assess soft skills and cultural fit:

```python
response = agent.generate_questions(
    resume_text=resume_text,
    job_description=job_description,
    round_type=RoundType.BEHAVIORAL,
    difficulty=DifficultyLevel.INTERMEDIATE,
    num_questions=10
)
```

### 3. System Design

For senior roles, test architectural thinking:

```python
response = agent.generate_questions(
    resume_text=resume_text,
    job_description=job_description,
    round_type=RoundType.SYSTEM_DESIGN,
    difficulty=DifficultyLevel.ADVANCED,
    num_questions=5
)
```

### 4. Coding Challenge

Generate algorithm and data structure problems:

```python
response = agent.generate_questions(
    resume_text=resume_text,
    job_description=job_description,
    round_type=RoundType.CODING,
    difficulty=DifficultyLevel.INTERMEDIATE,
    num_questions=8
)
```

## Tips for Best Results

### 1. Provide Detailed Job Descriptions

Better input = better questions:

```
✅ Good:
"Senior Python Developer with 5+ years experience.
Required: Django, PostgreSQL, AWS, Docker.
Will build microservices handling 10M+ requests/day."

❌ Too vague:
"Python developer needed"
```

### 2. Use Appropriate Difficulty Levels

- **Beginner**: 0-2 years experience
- **Intermediate**: 2-5 years experience
- **Advanced**: 5-8 years experience
- **Expert**: 8+ years, leadership roles

### 3. Specify Focus Areas

When you want questions on specific technologies:

```bash
--focus-areas "Kubernetes,Docker,Terraform,AWS"
```

### 4. Adjust Number of Questions

- **Phone screen**: 5-8 questions
- **Technical round**: 10-15 questions
- **Full interview**: 15-20 questions

### 5. Combine Multiple Rounds

Generate questions for each interview stage:

1. Technical screening (10 questions)
2. Behavioral (8 questions)
3. System design (3-5 questions)
4. Coding challenge (5 problems)

## Troubleshooting

### Issue: "OpenAI API key not found"

**Solution**: Make sure `.env` file exists with `OPENAI_API_KEY=...`

### Issue: "Failed to parse resume"

**Solution**: 
- Ensure PDF is not password-protected
- Try a different PDF
- Check if PDF contains actual text (not scanned image)

### Issue: "Rate limit exceeded"

**Solution**: 
- Wait a moment and retry
- Check your OpenAI API usage limits
- Consider using a higher-tier API key

### Issue: Questions are too generic

**Solution**:
- Provide more detailed job description
- Use `--focus-areas` to specify technologies
- Increase temperature in config (0.7-0.9)

### Issue: Import errors

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Next Steps

1. Read the [Architecture Documentation](docs/architecture.md)
2. Explore [API Reference](docs/api_reference.md)
3. Check out [Prompt Engineering Guide](docs/prompts.md)
4. Customize prompts for your needs
5. Integrate with your ATS or interview platform

## Getting Help

- Check the [README](../README.md) for detailed information
- Review example scripts in `examples/`
- Read the [Architecture docs](docs/architecture.md)
- Open an issue on GitHub for bugs or questions

## What's Next?

Try these advanced features:

1. **Batch Processing**: Generate questions for multiple candidates
2. **Custom Prompts**: Modify prompt templates for your company
3. **API Integration**: Integrate with your existing systems
4. **Automation**: Build workflows with the API

Happy interviewing! 🎯
