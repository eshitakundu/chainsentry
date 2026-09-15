# NOOA Mini Lab

A small experiment with NVIDIA NOOA to understand how an agent can interact with and modify the state of a Python object.

The project simulates a workspace containing unorganized files. A NOOA agent inspects the files, decides where they belong, moves them into categories, and verifies the final workspace state.

## Example

Initial workspace:

```text
unfiled/
├── annual_report.pdf
├── vacation_photo.png
├── analysis.py
├── sales_2026.csv
└── project_ideas.md
```

After the agent runs:

```text
documents/
└── annual_report.pdf

images/
└── vacation_photo.png

code/
└── analysis.py

data/
└── sales_2026.csv

notes/
└── project_ideas.md
```

The files are simulated in memory. No real files on the computer are modified.

## How It Works

The agent is defined using NVIDIA NOOA:

```python
class WorkspaceOrganizerAgent(Agent, llm=llm):
```

It has normal Python methods such as:

```python
list_files()
inspect_file()
move_file()
get_workspace_state()
```

These methods interact with the workspace state.

The main agentic method is:

```python
async def organize_workspace(self) -> OrganizeReport:
    ...
```

The `...` delegates the method to NOOA.

The agent can then decide which Python methods to call and in what order.

```text
list files
    ↓
inspect file
    ↓
choose destination
    ↓
move file
    ↓
repeat
    ↓
verify final state
```

The important part is that the agent does not only generate a recommendation.

It calls `move_file()` and changes the Python object's state.

## NOOA Concepts Used

### Agent

```python
class WorkspaceOrganizerAgent(Agent, llm=llm):
```

The Python class becomes a NOOA agent.

### Python Capabilities

Methods such as:

```python
def move_file(...):
```

contain normal Python code and perform the actual actions.

### LLM-Driven Method

```python
async def organize_workspace(...):
    ...
```

NOOA uses the configured LLM to execute this task.

### Structured Output

The result follows a Pydantic model:

```python
class OrganizeReport(BaseModel):
    actions_taken: list[str]
    summary: str
```

## Tech Stack

* Python
* NVIDIA NOOA
* OpenRouter
* Pydantic
* python-dotenv
* uv

## Setup

Clone the repository:

```bash
git clone https://github.com/eshitakundu/nooa-mini-lab.git
cd nooa-mini-lab
```

Install dependencies:

```bash
uv sync
```

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

Run the project:

```bash
uv run main.py
```

## Sample Output

```text
BEFORE

unfiled:
- annual_report.pdf
- vacation_photo.png
- analysis.py
- sales_2026.csv
- project_ideas.md

NOOA AGENT RUNNING...

AFTER

documents:
- annual_report.pdf

images:
- vacation_photo.png

code:
- analysis.py

data:
- sales_2026.csv

notes:
- project_ideas.md
```

## What I Learned

This project helped me understand the basic NOOA execution model:

```text
agent
  ↓
inspect live Python state
  ↓
choose a method
  ↓
execute Python action
  ↓
state changes
  ↓
continue until task is complete
```

The next step is to use the same pattern with real tools, external data, and larger agentic applications.