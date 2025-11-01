# Interview Assistant AI Agent

An intelligent AI-powered system that assists interviewers by generating tailored interview questions based on candidate resumes, job descriptions, and interview rounds.

## 🎯 Features

- **Resume Parsing**: Automatically extracts information from PDF resumes
- **AI-Powered Question Generation**: Uses Google Gemini API to create relevant interview questions
- **Multiple Interview Types**: Supports technical, behavioral, system design, and coding rounds
- **Difficulty Levels**: Generates questions ranging from beginner to advanced
- **Job-Specific**: Tailors questions based on job description requirements
- **REST API**: Easy-to-use API for integration with existing systems

## 🏗️ Architecture

```
interview_assistant/
├── src/
│   ├── agent/          # Gemini AI agent implementation
│   ├── parsers/        # Resume and document parsers
│   ├── models/         # Pydantic data models
│   ├── prompts/        # Prompt templates
│   └── api/            # FastAPI endpoints
├── examples/           # Sample resumes and job descriptions
├── tests/              # Test suite
└── docs/               # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
cd interview_assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Google Gemini API key
```

### Configuration

Create a `.env` file with the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key_here
MODEL_NAME=gemini-2.5-flash
TEMPERATURE=0.7
MAX_TOKENS=2000
```

To get a Gemini API key:
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

## 💻 Usage

### Python API

```python
from src.agent.interview_agent import InterviewQuestionAgent
from src.parsers.resume_parser import ResumeParser

# Parse resume
parser = ResumeParser()
resume_data = parser.parse_pdf("path/to/resume.pdf")

# Generate questions
agent = InterviewQuestionAgent()
questions = agent.generate_questions(
    resume_text=resume_data,
    job_description="Senior Python Developer...",
    round_type="technical",
    difficulty="intermediate",
    num_questions=10
)

for q in questions:
    print(f"Q: {q['question']}")
    print(f"Category: {q['category']}")
    print(f"Difficulty: {q['difficulty']}\n")
```

### REST API

Start the API server:

```bash
uvicorn src.api.main:app --reload
```

Then make requests:

```bash
# Upload resume and generate questions
curl -X POST "http://localhost:8000/api/v1/generate-questions" \
  -H "Content-Type: multipart/form-data" \
  -F "resume=@resume.pdf" \
  -F "job_description=Senior Python Developer..." \
  -F "round_type=technical" \
  -F "difficulty=intermediate" \
  -F "num_questions=10"
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 📚 Interview Round Types

- **technical**: Technical skills and coding knowledge
- **behavioral**: Soft skills and cultural fit
- **system_design**: Architecture and design questions
- **coding**: Live coding and algorithm challenges
- **domain_specific**: Industry-specific questions

## 🎯 Question Difficulty Levels

- **beginner**: Entry-level questions
- **intermediate**: Mid-level questions
- **advanced**: Senior-level questions
- **expert**: Architect/Staff-level questions

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

## 📖 Documentation

Detailed documentation is available in the `docs/` directory:

- [Architecture Overview](docs/architecture.md)
- [API Reference](docs/api_reference.md)
- [Prompt Engineering Guide](docs/prompts.md)
- [Contributing Guidelines](docs/contributing.md)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](docs/contributing.md) before submitting PRs.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔒 Privacy & Security

- Resumes are processed in-memory and not stored
- All API calls to Google Gemini are encrypted
- No candidate data is logged or persisted
- Compliant with GDPR and privacy best practices

## 🌟 Acknowledgments

Built with:
- [Google Gemini API](https://ai.google.dev/gemini-api) - Language model
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF parsing

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.
