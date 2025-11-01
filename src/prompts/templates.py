"""Prompt templates for different interview types."""

from typing import Dict, List


class SimplePromptTemplate:
    """Simple prompt template replacement for LangChain PromptTemplate."""
    
    def __init__(self, template: str, input_variables: List[str]):
        self.template = template
        self.input_variables = input_variables
    
    def format(self, **kwargs) -> str:
        """Format the template with provided variables."""
        return self.template.format(**kwargs)


TECHNICAL_INTERVIEW_PROMPT = SimplePromptTemplate(
    input_variables=["resume", "job_description", "difficulty", "num_questions", "focus_areas"],
    template="""You are an expert technical interviewer with years of experience evaluating candidates.

Your task is to generate {num_questions} high-quality technical interview questions based on the following:

CANDIDATE RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

DIFFICULTY LEVEL: {difficulty}
{focus_areas}

Generate questions that:
1. Are relevant to both the candidate's experience and the job requirements
2. Match the specified difficulty level
3. Test both theoretical knowledge and practical skills
4. Cover a diverse range of topics from the resume and job description
5. Are specific and actionable (avoid generic questions)

For each question, provide:
- The question text
- Category (e.g., Python, System Design, Databases, etc.)
- Expected topics the answer should cover
- 1-2 follow-up questions to dive deeper

Format your response as a JSON array with this structure:
[
  {{
    "question": "Question text here",
    "category": "Category name",
    "difficulty": "{difficulty}",
    "expected_topics": ["topic1", "topic2"],
    "follow_up_questions": ["follow-up 1", "follow-up 2"]
  }}
]

Generate exactly {num_questions} questions."""
)


BEHAVIORAL_INTERVIEW_PROMPT = SimplePromptTemplate(
    input_variables=["resume", "job_description", "difficulty", "num_questions"],
    template="""You are an expert HR interviewer skilled at assessing cultural fit and soft skills.

Your task is to generate {num_questions} behavioral interview questions based on:

CANDIDATE RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

DIFFICULTY LEVEL: {difficulty}

Generate questions that:
1. Use the STAR method (Situation, Task, Action, Result)
2. Assess leadership, teamwork, problem-solving, and communication skills
3. Are relevant to the candidate's experience level
4. Evaluate cultural fit for the role
5. Explore both successes and challenges

For each question, provide:
- The question text
- Category (e.g., Leadership, Teamwork, Problem-solving, etc.)
- What you're evaluating with this question
- Follow-up probes

Format your response as a JSON array with this structure:
[
  {{
    "question": "Tell me about a time when...",
    "category": "Category name",
    "difficulty": "{difficulty}",
    "context": "What this question evaluates",
    "follow_up_questions": ["follow-up 1", "follow-up 2"]
  }}
]

Generate exactly {num_questions} questions."""
)


SYSTEM_DESIGN_PROMPT = SimplePromptTemplate(
    input_variables=["resume", "job_description", "difficulty", "num_questions"],
    template="""You are a senior architect conducting a system design interview.

Your task is to generate {num_questions} system design questions based on:

CANDIDATE RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

DIFFICULTY LEVEL: {difficulty}

Generate questions that:
1. Test architectural thinking and scalability concepts
2. Are appropriate for the candidate's experience level
3. Cover topics like: distributed systems, databases, caching, load balancing, microservices
4. Require the candidate to make trade-offs and justify decisions
5. Are realistic and practical (not just theoretical)

For each question, provide:
- The design challenge
- Category (e.g., Distributed Systems, Database Design, etc.)
- Key topics to discuss
- Important trade-offs to consider

Format your response as a JSON array with this structure:
[
  {{
    "question": "Design a system that...",
    "category": "Category name",
    "difficulty": "{difficulty}",
    "expected_topics": ["scalability", "data consistency", "etc"],
    "follow_up_questions": ["How would you handle...", "What if traffic increased..."]
  }}
]

Generate exactly {num_questions} questions."""
)


CODING_INTERVIEW_PROMPT = SimplePromptTemplate(
    input_variables=["resume", "job_description", "difficulty", "num_questions"],
    template="""You are conducting a coding interview focused on algorithms and data structures.

Your task is to generate {num_questions} coding problems based on:

CANDIDATE RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

DIFFICULTY LEVEL: {difficulty}

Generate problems that:
1. Test algorithmic thinking and problem-solving skills
2. Are appropriate for the difficulty level
3. Cover various topics: arrays, strings, trees, graphs, dynamic programming, etc.
4. Have clear problem statements and constraints
5. Are relevant to the technologies mentioned in the resume

For each problem, provide:
- The problem statement
- Category (e.g., Arrays, Trees, Dynamic Programming, etc.)
- Hints for the optimal approach
- Time/space complexity expectations

Format your response as a JSON array with this structure:
[
  {{
    "question": "Write a function that...",
    "category": "Category name",
    "difficulty": "{difficulty}",
    "expected_topics": ["approach hint", "complexity expectation"],
    "follow_up_questions": ["How would you optimize...", "What if constraints changed..."]
  }}
]

Generate exactly {num_questions} questions."""
)


DOMAIN_SPECIFIC_PROMPT = SimplePromptTemplate(
    input_variables=["resume", "job_description", "difficulty", "num_questions", "domain"],
    template="""You are a domain expert conducting a specialized technical interview.

Your task is to generate {num_questions} domain-specific questions based on:

CANDIDATE RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

DOMAIN FOCUS: {domain}
DIFFICULTY LEVEL: {difficulty}

Generate questions that:
1. Are highly relevant to the specific domain
2. Test both theoretical knowledge and practical experience
3. Match the candidate's experience level
4. Cover best practices and common challenges in the domain
5. Require deep understanding, not just surface knowledge

For each question, provide:
- The question text
- Category within the domain
- Key concepts to evaluate
- Follow-up questions to probe deeper

Format your response as a JSON array with this structure:
[
  {{
    "question": "Question text here",
    "category": "Category name",
    "difficulty": "{difficulty}",
    "expected_topics": ["topic1", "topic2"],
    "follow_up_questions": ["follow-up 1", "follow-up 2"]
  }}
]

Generate exactly {num_questions} questions."""
)


# Mapping of round types to prompts
PROMPT_TEMPLATES = {
    "technical": TECHNICAL_INTERVIEW_PROMPT,
    "behavioral": BEHAVIORAL_INTERVIEW_PROMPT,
    "system_design": SYSTEM_DESIGN_PROMPT,
    "coding": CODING_INTERVIEW_PROMPT,
    "domain_specific": DOMAIN_SPECIFIC_PROMPT,
}
