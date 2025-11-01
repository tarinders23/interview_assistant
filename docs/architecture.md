# Interview Assistant Architecture

## Overview

The Interview Assistant is an AI-powered system that generates contextual interview questions based on candidate resumes and job descriptions. It uses LangChain with OpenAI's GPT-4 to create intelligent, relevant questions for various interview rounds.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  (CLI, API Clients, Web UI, Postman, cURL)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Endpoints:                                           │  │
│  │  - POST /api/v1/generate-questions                   │  │
│  │  - POST /api/v1/generate-questions-json              │  │
│  │  - POST /api/v1/parse-resume                         │  │
│  │  - GET  /health                                       │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
│  ┌──────────────────────┐      ┌──────────────────────┐    │
│  │  Resume Parser       │      │  Question Agent      │    │
│  │  (pdfplumber)        │      │  (LangChain + GPT-4) │    │
│  └──────────────────────┘      └──────────────────────┘    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              OpenAI API (GPT-4)                       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. API Layer (`src/api/`)

**FastAPI Application**: Provides RESTful endpoints for the system.

Key features:
- File upload handling for PDF resumes
- Request validation using Pydantic
- Error handling and logging
- CORS support for web clients
- Interactive API documentation (Swagger UI)

### 2. Business Logic Layer

#### Resume Parser (`src/parsers/`)

**Purpose**: Extract structured information from PDF resumes.

**Technology**: pdfplumber

**Capabilities**:
- Extract text from multi-page PDFs
- Parse contact information (email, phone)
- Identify technical skills using keyword matching
- Handle various PDF formats and layouts
- Graceful error handling

**Future Enhancements**:
- Named Entity Recognition (NER) for better extraction
- Support for DOCX format
- Experience timeline extraction
- Education details parsing

#### Question Agent (`src/agent/`)

**Purpose**: Generate contextual interview questions using AI.

**Technology**: LangChain + OpenAI GPT-4

**Process Flow**:
1. Receive resume text, job description, and parameters
2. Select appropriate prompt template based on round type
3. Construct context-aware prompt with all inputs
4. Call GPT-4 via LangChain
5. Parse and validate response
6. Return structured questions

**Prompt Templates** (`src/prompts/`):
- Technical interviews
- Behavioral interviews
- System design interviews
- Coding challenges
- Domain-specific questions

### 3. Data Models (`src/models/`)

**Pydantic Models** for type safety and validation:

- `ResumeData`: Parsed resume information
- `JobDescription`: Job posting details
- `InterviewQuestion`: Generated question with metadata
- `QuestionGenerationRequest`: API request payload
- `QuestionGenerationResponse`: API response payload
- `RoundType`: Enum for interview types
- `DifficultyLevel`: Enum for question difficulty

## Data Flow

### Question Generation Flow

```
1. Client uploads resume PDF + job description
           ↓
2. API validates inputs and file type
           ↓
3. Resume Parser extracts text from PDF
           ↓
4. Question Agent receives:
   - Resume text
   - Job description
   - Round type
   - Difficulty level
   - Number of questions
           ↓
5. Agent selects appropriate prompt template
           ↓
6. LangChain constructs prompt with context
           ↓
7. GPT-4 generates questions in JSON format
           ↓
8. Agent parses and validates response
           ↓
9. Structured questions returned to client
```

## Key Design Decisions

### 1. LangChain Framework

**Why LangChain?**
- Standardized interface for LLMs
- Built-in prompt management
- Easy to swap models or providers
- Excellent debugging and observability
- Active community and updates

### 2. Pydantic for Data Validation

**Benefits**:
- Type safety at runtime
- Automatic validation
- Clear error messages
- JSON serialization
- IDE autocomplete support

### 3. FastAPI Framework

**Advantages**:
- High performance (async support)
- Automatic API documentation
- Built-in request validation
- Easy to test
- Modern Python features

### 4. pdfplumber for PDF Parsing

**Why pdfplumber?**
- Pure Python implementation
- Handles complex layouts
- Extract text and tables
- Better than PyPDF2 for most cases
- Active maintenance

## Configuration Management

Uses Pydantic Settings for environment-based configuration:

```python
class Settings(BaseSettings):
    openai_api_key: str
    model_name: str = "gpt-4-turbo"
    temperature: float = 0.7
    max_tokens: int = 2000
    # ...
```

Configuration sources (in order of precedence):
1. Environment variables
2. .env file
3. Default values

## Error Handling Strategy

### Layered Error Handling:

1. **Input Validation**: Pydantic models catch invalid data
2. **Business Logic**: Custom exceptions for domain errors
3. **External Services**: Retry logic and graceful degradation
4. **API Layer**: HTTP status codes and error messages

### Error Types:

- `ResumeParserError`: PDF parsing failures
- `InterviewAgentError`: Question generation failures
- `HTTPException`: API-level errors

## Security Considerations

1. **API Keys**: Stored in environment variables, never in code
2. **File Upload**: Validate file types and sizes
3. **Data Privacy**: Resumes processed in-memory, not persisted
4. **Input Sanitization**: All inputs validated via Pydantic
5. **CORS**: Configurable allowed origins
6. **Rate Limiting**: Can be added via middleware

## Scalability Considerations

### Current Architecture:
- Single-instance deployment
- Synchronous processing
- In-memory resume processing

### Future Scaling Options:

1. **Horizontal Scaling**:
   - Deploy multiple API instances
   - Use load balancer (nginx, ALB)
   - Shared configuration via environment

2. **Async Processing**:
   - Add job queue (Celery, RQ)
   - Background question generation
   - Webhook callbacks for completion

3. **Caching**:
   - Cache common job descriptions
   - Cache parsed resumes (with TTL)
   - Redis for distributed cache

4. **Database**:
   - Store generated questions
   - Track usage analytics
   - User authentication

## Monitoring and Observability

### Current Logging:
- Python logging module
- Configurable log levels
- Structured log messages

### Recommended Additions:
- **APM**: DataDog, New Relic, or Sentry
- **Metrics**: Prometheus + Grafana
- **Tracing**: OpenTelemetry
- **LLM Observability**: LangSmith

## Testing Strategy

### Unit Tests:
- Test individual components
- Mock external dependencies
- Fast execution

### Integration Tests:
- Test component interactions
- Use test API keys
- Validate end-to-end flows

### API Tests:
- Test all endpoints
- Validate error handling
- Check response schemas

## Deployment Options

### Local Development:
```bash
uvicorn src.api.main:app --reload
```

### Production Deployment:

1. **Docker Container**:
   ```dockerfile
   FROM python:3.10
   COPY . /app
   RUN pip install -r requirements.txt
   CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0"]
   ```

2. **Cloud Platforms**:
   - AWS: ECS, Lambda, or EC2
   - GCP: Cloud Run or App Engine
   - Azure: App Service or Container Instances
   - Heroku: Simple deployment

3. **Kubernetes**:
   - Scalable deployment
   - Load balancing
   - Auto-scaling

## Future Enhancements

1. **Multi-Language Support**: Questions in different languages
2. **Question Bank**: Store and reuse questions
3. **Candidate Profiles**: Save candidate information
4. **Interview Scheduling**: Integration with calendars
5. **Feedback Loop**: Improve questions based on interviewer feedback
6. **Video Interview**: Generate questions for video platforms
7. **Skill Assessment**: Automated scoring of responses
8. **Company Customization**: Company-specific question styles

## Dependencies

### Core Dependencies:
- `langchain`: AI agent framework
- `langchain-openai`: OpenAI integration
- `openai`: OpenAI API client
- `pdfplumber`: PDF parsing
- `fastapi`: Web framework
- `pydantic`: Data validation
- `python-dotenv`: Environment management

### Development Dependencies:
- `pytest`: Testing framework
- `black`: Code formatting
- `flake8`: Linting
- `mypy`: Type checking
