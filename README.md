## About the Project

The Daily Schedule Agent allows a user to describe their activities in normal language.

For example:

> I have college from 9 AM to 4 PM, study Python for 2 hours, work on my project for 2 hours, and exercise for 1 hour.

The system uses Gemini to understand the user's input and extract the tasks. Python then handles task prioritization, scheduling, and validation.

The project is intentionally basic because the main goal is to understand the fundamental building blocks of an AI agent before moving to more advanced Agentic AI systems.

## How It Works

The system follows this workflow:

```text
User Input
    ↓
Gemini LLM
    ↓
Task Extraction
    ↓
Structured JSON
    ↓
Pydantic Validation
    ↓
Task Prioritization
    ↓
Schedule Planning
    ↓
Schedule Validation
    ↓
Final Schedule

1. User Input
The user describes their activities in natural language.
Example:
I need to study Python for 2 hours, work on my project for 3 hours,
and exercise for 1 hour.

2. Task Extraction
Gemini converts the natural-language input into structured task information.
Each task contains:
- Task name
- Duration
- Priority
- Fixed start time
- Fixed end time
Example:
{
    "name": "Study Python",
    "duration": 2,
    "priority": 2,
    "fixed_start": null,
    "fixed_end": null
}

3. Validation
Pydantic validates the extracted task information and ensures that the data follows the expected structure.
4. Prioritization
Tasks are prioritized using:
1 → High
2 → Medium
3 → Low

Higher-priority tasks are considered first when creating the schedule.
5. Schedule Planning
The Python scheduler identifies available time slots and places flexible tasks around fixed activities.
For example:
09:00 - 16:00 → College
16:00 - 18:00 → Study Python
18:00 - 18:15 → Break
18:15 - 20:15 → Work on Project

6. Schedule Validation
The system checks the generated schedule for problems such as:
- Overlapping activities
- Missing tasks
- Invalid time ranges
- Insufficient available time
If a task cannot fit into the available time, the system reports it instead of generating an incorrect schedule.
Example:
College: 09:00 - 16:00
Project: 10 hours

Result:
Project → Not scheduled
Reason: Not enough available time

Agentic AI Concepts Learned
This project helped me understand the basic components of an AI agent:
- Perception: understanding the user's request
- Structured state: representing tasks in a consistent format
- Reasoning: prioritizing tasks
- Planning: creating a schedule
- Action: placing tasks into available time slots
- Validation: checking whether the generated plan is valid
- Error handling: handling API failures and impossible schedules
The important design decision in this project is that the LLM is mainly responsible for understanding the user's natural-language request. The actual scheduling logic is handled by Python.
Gemini
  ↓
Understand the request
  ↓
Extract structured tasks
  ↓
Python
  ↓
Plan and schedule
  ↓
Validate

This separation makes the system easier to understand and control.
Technologies Used
- Python
- Gemini API
- Google GenAI SDK
- Pydantic
- python-dotenv
- JSON
- Git
- GitHub
Project Structure
daily-schedule-agent/
│
├── main.py
├── models.py
├── planner.py
├── validator.py
├── llm_parser.py
│
├── data/
│
├── .gitignore
└── README.md

File Description
main.py
Runs the complete agent workflow.
models.py
Contains the Pydantic task model.
llm_parser.py
Connects to Gemini and converts natural-language input into structured tasks.
planner.py
Handles task prioritization and schedule creation.
validator.py
Checks the generated schedule for conflicts and errors.
Example
Input:
I need to study Python for 2 hours with high priority,
work on my project for 2 hours with medium priority,
and exercise for 1 hour with low priority.

Output:
08:00 - 10:00 → Study Python
10:00 - 10:15 → Break
10:15 - 12:15 → Work on Project
12:15 - 12:30 → Break
12:30 - 13:30 → Exercise

Current Limitations
This is a foundational project and does not currently include:
- Long-term memory
- Database storage
- Multiple agents
- Advanced tool calling
- Calendar integration
- Autonomous background execution
- Agent-to-agent communication
- Production deployment
These concepts will be explored in future projects.
Future Learning
My Agentic AI learning path will gradually move from simple agents to more advanced systems involving:
Basic Agents
    ↓
Memory
    ↓
Tools and APIs
    ↓
Planning
    ↓
Multi-Agent Systems
    ↓
Autonomous Workflows
    ↓
Evaluation and Safety
    ↓
Production AI Agents

Learning Journey
This project is intentionally simple because it is my first practical step into Agentic AI.
I have already worked with Python, Generative AI, LLMs, and RAG. With this project, I am beginning the next stage of my learning journey: understanding how AI systems can perceive information, reason about tasks, make plans, take actions, and validate their results.
The goal is to build progressively more capable Agentic AI systems through practical projects rather than jumping directly into complex architectures.