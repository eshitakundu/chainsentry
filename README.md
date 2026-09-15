# NOOA Mini Lab

A minimal hands-on experiment with NVIDIA NOOA (Object-Oriented Agents).

This repository explores a simple but important agentic concept:

> An LLM does not have to only generate text. It can operate through methods on a live Python object and change the state of that object.

The project implements a small autonomous workspace organizer.

It runs entirely in the terminal and uses a simulated workspace, making it easy to understand the core NOOA programming model without adding APIs, databases, frontends, or other infrastructure.

---

## What It Does

The program starts with a simulated workspace containing unorganized files:

```text
annual_report.pdf
vacation_photo.png
analysis.py
sales_2026.csv
project_ideas.md
```

Initially, every file is:

```text
unfiled
```

A NOOA agent is given capabilities to:

```text
list files
inspect files
move files
inspect the current workspace state
```

The agent must autonomously determine where the files belong and organize them.

For example:

```text
annual_report.pdf
        ↓
documents

vacation_photo.png
        ↓
images

analysis.py
        ↓
code

sales_2026.csv
        ↓
data

project_ideas.md
        ↓
notes
```

---

# Why This Is More Than a Prompt

A basic LLM application often looks like:

```text
prompt
  ↓
LLM
  ↓
text
```

The model receives information and generates an answer.

This experiment is different.

```text
             Workspace state
                   ▲
                   │
                   ▼
          WorkspaceOrganizerAgent
                   │
          ┌────────┼─────────┐
          │        │         │
          ▼        ▼         ▼
       inspect    move      verify
          │        │         │
          └────────┼─────────┘
                   │
                   ▼
               NOOA agent
```

The agent does not simply say:

```text
"analysis.py should go into the code folder"
```

It can actually execute:

```python
self.move_file(
    "analysis.py",
    "code",
)
```

That method changes the state of the Python object.

The environment before and after the agent runs is therefore different.

---

# Architecture

```text
                    main.py
                       │
                       ▼
              WorkspaceOrganizerAgent
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   list_files()   inspect_file()   move_file()
        │              │              │
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
                live Python state
                       ▲
                       │
                       ▼
               organize_workspace()
                       │
                      ...
                       │
                       ▼
                  NVIDIA NOOA
                       │
                       ▼
                    OpenRouter
                       │
                       ▼
              autonomous actions
                       │
                       ▼
               modified workspace
```

---

# Core NOOA Idea

The agent is defined as:

```python
class WorkspaceOrganizerAgent(
    Agent,
    llm=llm,
):
```

`Agent` comes from NVIDIA NOOA.

The object contains both:

```text
normal Python methods
```

and:

```text
LLM-driven methods
```

---

## Normal Python Capabilities

The following methods contain ordinary Python implementations:

```python
list_files()
inspect_file()
move_file()
get_workspace_state()
```

For example:

```python
def move_file(
    self,
    filename: str,
    destination: str,
) -> str:
```

This method actually modifies:

```python
self._workspace
```

There is no LLM involved in performing the state update.

Python performs the action.

---

# The NOOA Method

The main agentic method is:

```python
async def organize_workspace(
    self,
) -> OrganizeReport:
    ...
```

The body contains:

```python
...
```

Rather than implementing the procedure manually, the task is delegated through NOOA to the configured LLM strategy.

The method's docstring tells the agent what it needs to accomplish:

```text
inspect the workspace

move every unfiled file

verify the final state
```

The agent determines which capabilities it needs to call and in what order.

---

# Agent Interaction

A possible execution sequence is:

```text
organize_workspace()

    ↓

list_files()

    ↓

inspect_file("annual_report.pdf")

    ↓

move_file(
    "annual_report.pdf",
    "documents"
)

    ↓

inspect_file("analysis.py")

    ↓

move_file(
    "analysis.py",
    "code"
)

    ↓

...

    ↓

get_workspace_state()

    ↓

return OrganizeReport
```

The exact sequence is decided by the agent.

---

# Live State

The simulated workspace exists inside the agent:

```python
self._workspace
```

Before execution:

```json
{
  "unfiled": [
    "annual_report.pdf",
    "vacation_photo.png",
    "analysis.py",
    "sales_2026.csv",
    "project_ideas.md"
  ]
}
```

After execution, the same Python object has been modified.

For example:

```json
{
  "unfiled": [],
  "documents": [
    "annual_report.pdf"
  ],
  "images": [
    "vacation_photo.png"
  ],
  "code": [
    "analysis.py"
  ],
  "data": [
    "sales_2026.csv"
  ],
  "notes": [
    "project_ideas.md"
  ]
}
```

The final workspace state printed by the program comes directly from Python.

It is not generated by the LLM.

---

# Structured Output

The agent also returns:

```python
class OrganizeReport(BaseModel):
    actions_taken: list[str]
    summary: str
```

This means the final agent response has a predictable structure.

Example:

```json
{
  "actions_taken": [
    "Moved annual_report.pdf to documents",
    "Moved vacation_photo.png to images",
    "Moved analysis.py to code",
    "Moved sales_2026.csv to data",
    "Moved project_ideas.md to notes"
  ],
  "summary": "All workspace files were successfully organized."
}
```

---

# OpenRouter

The LLM is configured using:

```python
llm = get_llm_client(
    "openrouter/auto"
)
```

The OpenRouter API key is loaded from:

```text
.env
```

using:

```python
load_dotenv()
```

The API key is never committed to Git.

---

# Project Structure

```text
nooa-mini-lab/
│
├── main.py
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── .env
```

`.env` and `.venv/` remain local.

---

# Setup

The project is developed using Linux / WSL2.

Clone the repository:

```bash
git clone https://github.com/eshitakundu/nooa-mini-lab.git
cd nooa-mini-lab
```

Install dependencies:

```bash
uv sync
```

Create:

```text
.env
```

and add:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

Run:

```bash
uv run main.py
```

---

# Tech Stack

- Python
- NVIDIA NOOA
- OpenRouter
- LiteLLM
- Pydantic
- python-dotenv
- uv

---

# What This Demonstrates

This experiment focuses on a few core concepts:

```text
NOOA Agent
      +
live Python object
      +
callable Python methods
      +
state mutation
      +
LLM-selected actions
      +
structured output
```

It intentionally avoids unnecessary complexity.

There is:

```text
no frontend
no database
no external API
no RAG
no multi-agent system
```

The goal is simply to understand what makes an object-oriented agent different from a normal prompt-response application.

---

# Limitations

The workspace is simulated entirely in memory.

No real files on the computer are moved or modified.

This is intentional.

It allows the NOOA interaction model to be explored without giving an experimental LLM permission to alter the real filesystem.

---

# Next Step

This repository is the first step in a larger learning progression:

```text
NOOA Mini Lab
     │
     │ basic object-oriented agent
     ▼
Agentic Application
     │
     │ multiple capabilities + frontend
     ▼
ChainSentry
     │
     │ real blockchain APIs + agents
     ▼
Web3 / smart-contract extensions
```

---

# Key Takeaway

The important difference is:

```text
LLM application:
prompt → text

NOOA experiment:
environment ↔ agent ↔ actions
```

The model is not only describing what should happen.

It is using methods on a live Python object to make it happen.