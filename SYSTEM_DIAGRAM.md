# Interview Assistant - Visual System Overview

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUTS                              │
│  • Resume PDF                                                    │
│  • Job Description                                               │
│  • Interview Type (technical/behavioral/system_design/etc)       │
│  • Difficulty Level (beginner/intermediate/advanced/expert)      │
│  • Number of Questions                                           │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ENTRY POINTS (Choose One)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   CLI Tool   │  │  Python API  │  │   REST API   │         │
│  │   cli.py     │  │   Direct     │  │   FastAPI    │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RESUME PARSER                                 │
│  src/parsers/resume_parser.py                                   │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Extract text from PDF (pdfplumber)                     │ │
│  │  • Identify name and email                                │ │
│  │  • Extract technical skills                               │ │
│  │  • Handle multiple pages                                  │ │
│  │  • Error handling for corrupt PDFs                        │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DATA VALIDATION                                 │
│  src/models/__init__.py                                         │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Validate input types (Pydantic)                        │ │
│  │  • Check constraints (1-50 questions)                     │ │
│  │  • Ensure valid enum values                               │ │
│  │  • Sanitize inputs                                        │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              PROMPT TEMPLATE SELECTION                           │
│  src/prompts/templates.py                                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Based on round_type, select:                             │ │
│  │  • TECHNICAL_INTERVIEW_PROMPT                             │ │
│  │  • BEHAVIORAL_INTERVIEW_PROMPT                            │ │
│  │  • SYSTEM_DESIGN_PROMPT                                   │ │
│  │  • CODING_INTERVIEW_PROMPT                                │ │
│  │  • DOMAIN_SPECIFIC_PROMPT                                 │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                AI QUESTION AGENT                                 │
│  src/agent/interview_agent.py                                   │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  1. Combine resume + job description + parameters         │ │
│  │  2. Fill prompt template with context                     │ │
│  │  3. Call LangChain with GPT-4                            │ │
│  │  4. Request structured JSON output                        │ │
│  │  5. Parse and validate response                           │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LANGCHAIN + GPT-4                              │
│  External Service (OpenAI)                                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Process natural language context                       │ │
│  │  • Generate contextual questions                          │ │
│  │  • Include follow-up questions                            │ │
│  │  • Identify expected topics                               │ │
│  │  • Return structured JSON                                 │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                  RESPONSE PROCESSING                             │
│  src/agent/interview_agent.py                                   │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Parse JSON response                                    │ │
│  │  • Create InterviewQuestion objects                       │ │
│  │  • Handle markdown code blocks                            │ │
│  │  • Validate question structure                            │ │
│  │  • Add metadata                                           │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                        OUTPUT                                    │
│  QuestionGenerationResponse                                     │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  {                                                         │ │
│  │    "questions": [                                          │ │
│  │      {                                                     │ │
│  │        "question": "What is...?",                          │ │
│  │        "category": "Python",                               │ │
│  │        "difficulty": "intermediate",                       │ │
│  │        "expected_topics": ["topic1", "topic2"],            │ │
│  │        "follow_up_questions": ["How...", "Why..."]         │ │
│  │      }                                                     │ │
│  │    ],                                                      │ │
│  │    "total_questions": 10,                                  │ │
│  │    "round_type": "technical",                              │ │
│  │    "difficulty": "intermediate"                            │ │
│  │  }                                                         │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

```
interview_assistant/
│
├── CLI Layer (cli.py)
│   └── Command-line argument parsing
│
├── API Layer (src/api/)
│   ├── FastAPI application
│   ├── Route handlers
│   ├── File upload handling
│   └── Error handling
│
├── Business Logic Layer
│   ├── Agent (src/agent/)
│   │   ├── LangChain integration
│   │   ├── Question generation logic
│   │   └── Response parsing
│   │
│   ├── Parsers (src/parsers/)
│   │   ├── PDF text extraction
│   │   ├── Information extraction
│   │   └── Skill detection
│   │
│   └── Prompts (src/prompts/)
│       └── Template management
│
├── Data Layer (src/models/)
│   ├── Request models
│   ├── Response models
│   ├── Domain models
│   └── Enums
│
└── Configuration Layer (src/config.py)
    └── Environment management
```

## Data Flow Example

### Example: Technical Interview Question Generation

```
1. INPUT
   ├── Resume: "Python developer, 5 years, Django, AWS"
   ├── Job: "Senior Backend Engineer"
   ├── Type: TECHNICAL
   ├── Difficulty: INTERMEDIATE
   └── Count: 10

2. PARSE RESUME
   ├── Extract text from PDF
   ├── Find: name, email, skills
   └── Output: ResumeData object

3. SELECT PROMPT
   └── Use: TECHNICAL_INTERVIEW_PROMPT

4. BUILD CONTEXT
   ├── Insert resume text
   ├── Insert job description
   ├── Add difficulty level
   ├── Add number of questions
   └── Add focus areas (if any)

5. CALL GPT-4
   ├── Send prompt via LangChain
   ├── Request JSON format
   └── Wait for response

6. PARSE RESPONSE
   ├── Extract JSON from markdown
   ├── Validate structure
   ├── Create InterviewQuestion objects
   └── Handle errors gracefully

7. OUTPUT
   └── QuestionGenerationResponse
       ├── 10 structured questions
       ├── Each with category
       ├── Each with follow-ups
       └── Each with expected topics
```

## Technology Stack

```
┌─────────────────────────────────────┐
│         Application Layer           │
│  ┌──────────┐  ┌──────────────┐    │
│  │   CLI    │  │   FastAPI    │    │
│  └──────────┘  └──────────────┘    │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         Framework Layer             │
│  ┌──────────────────────────────┐  │
│  │       LangChain 0.3+         │  │
│  │  (Agent orchestration)       │  │
│  └──────────────────────────────┘  │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         Service Layer               │
│  ┌──────────────────────────────┐  │
│  │      OpenAI GPT-4 API        │  │
│  │  (Language understanding)    │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘

Supporting Libraries:
├── pdfplumber (PDF parsing)
├── Pydantic 2.9+ (Data validation)
├── python-dotenv (Configuration)
└── Uvicorn (ASGI server)
```

## Question Generation Process

```
┌─────────────────────────────────────────────────┐
│  Step 1: Context Assembly                       │
│  ────────────────────────                       │
│  Resume:     "John Doe, Python dev..."          │
│  Job:        "Senior position..."               │
│  Difficulty: intermediate                       │
│  Count:      10                                 │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│  Step 2: Prompt Construction                    │
│  ────────────────────────                       │
│  Template: TECHNICAL_INTERVIEW_PROMPT           │
│  Variables: {resume, job_description, ...}      │
│  Result: "You are an expert interviewer..."     │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│  Step 3: LLM Call                               │
│  ────────────────                               │
│  Provider: OpenAI                               │
│  Model: gpt-4-turbo                             │
│  Temperature: 0.7                               │
│  Max tokens: 2000                               │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│  Step 4: Response Processing                    │
│  ────────────────────────                       │
│  Parse JSON: ✓                                  │
│  Validate structure: ✓                          │
│  Create objects: ✓                              │
│  Handle errors: ✓                               │
└────────┬────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│  Step 5: Output                                 │
│  ────────────────                               │
│  10 structured questions with:                  │
│  • Question text                                │
│  • Category                                     │
│  • Expected topics                              │
│  • Follow-up questions                          │
└─────────────────────────────────────────────────┘
```

## Error Handling Flow

```
┌────────────────────────────────────┐
│       User Request                 │
└───────────┬────────────────────────┘
            │
            ▼
┌────────────────────────────────────┐
│   Input Validation (Pydantic)     │
│   • Type checking                  │
│   • Range validation               │
│   • Enum validation                │
└───────┬────────────────────────────┘
        │ Valid
        ▼
┌────────────────────────────────────┐
│   Resume Parsing                   │
│   Try/Except:                      │
│   • FileNotFoundError              │
│   • PDFError                       │
│   • ValueError                     │
└───────┬────────────────────────────┘
        │ Success
        ▼
┌────────────────────────────────────┐
│   Question Generation              │
│   Try/Except:                      │
│   • OpenAI API errors              │
│   • Rate limit errors              │
│   • JSON parsing errors            │
└───────┬────────────────────────────┘
        │ Success
        ▼
┌────────────────────────────────────┐
│   Return Response                  │
└────────────────────────────────────┘

Any error at any stage:
└──────────▶ Log error
            ▼
            Return user-friendly error message
            ▼
            HTTP 400/500 or exception
```

## Deployment Architecture

```
Production Environment:
┌─────────────────────────────────────────────┐
│  Load Balancer (nginx/ALB)                  │
└────────────┬────────────────────────────────┘
             │
     ┌───────┴───────┐
     ▼               ▼
┌─────────┐     ┌─────────┐
│  API    │     │  API    │
│ Instance│     │ Instance│
│    1    │     │    2    │
└────┬────┘     └────┬────┘
     │               │
     └───────┬───────┘
             ▼
┌─────────────────────────────────────────────┐
│  External Services                          │
│  ┌─────────────────────────────────────┐   │
│  │  OpenAI API (GPT-4)                 │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘

Optional Additions:
├── Redis (for caching)
├── PostgreSQL (for question storage)
├── Monitoring (DataDog/New Relic)
└── Logging (CloudWatch/Splunk)
```

This visual overview provides a comprehensive understanding of how the Interview Assistant works from input to output.
