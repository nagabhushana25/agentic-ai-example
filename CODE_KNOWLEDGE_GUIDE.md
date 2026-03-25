# Code Knowledge Guide

This document is written to help you understand the project deeply enough to:

- read the code with confidence
- explain it to others
- present it in class or viva
- connect the code to agentic AI concepts

The goal of this guide is not only to say what each file does, but also:

- why that file is needed
- when it is used
- how it works in the whole system

## 1. First Understand the Big Picture

Before reading code, keep this one idea in mind:

This project is a `multi-agent workflow`.

That means:

- one part of the system does not do everything
- there is a central coordinator
- other components do specialized work
- all of them share information through a common state

In this project, the workflow is roughly:

1. user gives input
2. input is checked by guardrails
3. a shared state object is created
4. orchestrator decides what agent should work next
5. vector search agent fetches relevant knowledge
6. Databricks analyst agent handles structured analysis
7. final response is created
8. memory and session history are saved

That is the whole story of the system.

## 2. The Project As a Human Team

The easiest way to understand the code is to imagine it as a team:

- `main.py` = receptionist
- `guardrails.py` = security and screening desk
- `state.py` = shared notebook used by everyone
- `graph.py` = workflow map / manager
- `agents.py` = employees doing the real tasks
- `tools.py` = utility toolbox
- `memory_manager.py` = record keeper
- `config.py` = settings and environment desk

When you explain this to others, this analogy helps a lot.

## 3. Full File-by-File Understanding

## 3.1 `project/main.py`

File:
[project/main.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/main.py)

### Why this file is used

This is the entry point of the application.

Whenever you run:

```bash
python3 -m project.main
```

Python starts from this file.

### When it is used

It is used at the very beginning of program execution.

This file is responsible for:

- taking input from the user
- validating the input
- preparing the initial workflow state
- running the graph
- printing output

### What it does step by step

It does these things in order:

1. asks for `user_id`
2. asks for a prompt
3. checks input using guardrails
4. sanitizes the input
5. creates the initial state dictionary
6. builds the graph
7. runs the graph with that state
8. validates the output
9. prints final response and trace

### Why this design is useful

This keeps user interaction separate from business logic.

That means:

- user input logic stays here
- workflow logic stays in `graph.py`
- agent logic stays in `agents.py`

This is a clean design practice.

### How to explain it simply

You can say:

`main.py is the starting point that collects user input, prepares the initial data, runs the multi-agent workflow, and shows the result.`

## 3.2 `project/config.py`

File:
[project/config.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/config.py)

### Why this file is used

This file stores configuration and environment settings.

Instead of hardcoding values in many places, the project keeps important settings in one location.

### What kind of settings it stores

- OpenAI API key
- OpenAI model name
- Databricks host
- Databricks token
- tool call limit
- vector top-k result count
- paths to memory, skills, and knowledge folders

### When it is used

It is used whenever the app needs configuration.

Examples:

- graph needs paths and limits
- tools need access to directories
- OpenAI integration would need model and API key
- Databricks integration would need host and token

### Why this matters

Without a config file:

- values get repeated everywhere
- changes become harder
- environment setup becomes messy

With a config file:

- the project becomes organized
- setup becomes easier
- production-style design is clearer

### How to explain it simply

`config.py is the control panel of the project. It keeps all environment settings and important runtime values in one place.`

## 3.3 `project/state.py`

File:
[project/state.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/state.py)

### Why this file is used

This file defines the shared state of the workflow.

In LangGraph-style systems, the state is extremely important.

It is the object passed from one node to another.

### What “state” means here

State means the shared data that the whole workflow can read and update.

In this project, state contains things like:

- user input
- sanitized input
- which agent should run next
- retrieved context
- Databricks result
- final answer
- trace logs

### When it is used

It is used during the entire workflow.

Every node in the graph receives the state and may update part of it.

### Why it matters

Without state:

- agents cannot coordinate properly
- one agent will not know what another agent already did
- the workflow becomes hard to track

With state:

- each step can build on previous steps
- debugging becomes easier
- the design becomes structured and predictable

### Most important idea to remember

State is like a `shared notebook`.

Each agent writes something into the notebook, and the next agent reads it.

### How to explain it simply

`state.py defines the shared data structure used by all agents so they can work together in one workflow.`

## 3.4 `project/graph.py`

File:
[project/graph.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/graph.py)

### Why this file is used

This file defines the workflow using LangGraph.

It tells the program:

- where to start
- which nodes exist
- how control moves from one node to another

### When it is used

It is used after initial state is created in `main.py`.

The graph becomes the engine that runs the full workflow.

### What it contains

It contains:

- graph creation
- node registration
- edges between nodes
- conditional routing

### Nodes in this project

- `orchestrator`
- `vector_search`
- `databricks_analyst`
- `finalize`

### Flow in simple form

```text
START
  |
  v
orchestrator
  |
  |--- if vector search needed ---> vector_search ---> orchestrator
  |
  |--- if Databricks analysis needed ---> databricks_analyst ---> orchestrator
  |
  |--- if done ---> finalize ---> END
```

### Why it matters

This file is the heart of workflow orchestration.

It is what makes the project a `LangGraph-style application` instead of a normal script.

### How to explain it simply

`graph.py defines the state-machine workflow of the project. It decides how the system moves from one agent to another.`

## 3.5 `project/agents.py`

File:
[project/agents.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/agents.py)

### Why this file is used

This file contains the main agent logic.

This is where the actual “multi-agent behavior” lives.

### When it is used

It is used when `graph.py` runs nodes.

Each node in the graph usually points to a function in this file.

### Main parts inside this file

- `MiddlewareManager`
- `orchestrator_agent`
- `vector_search_agent`
- `databricks_analyst_agent`
- `finalize_response`

Now let us understand each one.

### 3.5.1 `MiddlewareManager`

### Why it is used

Middleware handles logic that is shared across the workflow.

Instead of writing the same extra behavior inside every agent, middleware centralizes common concerns.

### What middleware is doing here

This class simulates:

- todo tracking
- summarization
- tool call limiting
- retry policy note

### When it is used

It is used during graph execution, especially around node execution.

### Why it matters

Middleware is important in production systems because it handles cross-cutting concerns.

That means things that affect many parts of the system, not just one file.

Examples:

- logging
- retries
- limits
- summarization
- safety rules

### How to explain it simply

`MiddlewareManager adds system-level behavior that supports all agents, such as summarization and tool-call limits.`

### 3.5.2 `orchestrator_agent`

### Why it is used

This is the coordinator of the multi-agent workflow.

It is the most important agent in the system.

### What it does

- reads user memory
- checks current state
- chooses which agent should run next
- looks at skill library
- updates the trace

### When it is used

It is the first major node after the start.

It is also revisited after specialist agents complete their work.

### Why it matters

Without an orchestrator:

- there is no intelligent routing
- every agent would have to decide everything
- the workflow would become messy

The orchestrator is what makes the system feel coordinated.

### Current routing logic

In the current version:

- if no retrieved context exists, go to `vector_search`
- else if no Databricks result exists, go to `databricks_analyst`
- else go to `done`

### How to explain it simply

`The orchestrator agent acts like a manager. It checks what is already done and decides which specialist should work next.`

### 3.5.3 `vector_search_agent`

### Why it is used

This agent handles retrieval.

It searches local knowledge files and finds relevant text.

### What it does

- takes user request from state
- searches the knowledge directory
- gets relevant chunks
- stores those chunks back into state

### When it is used

It is used when the orchestrator decides that the system needs additional context.

### Why it matters

Without retrieval:

- final responses may be generic
- the system has no grounding in documents

With retrieval:

- the answer can use assignment-related context
- the architecture becomes closer to RAG systems

### How to explain it simply

`The vector search agent looks through project knowledge and brings back useful context for the workflow.`

### 3.5.4 `databricks_analyst_agent`

### Why it is used

This agent represents structured-data analysis.

It is meant for tasks where the system needs something like SQL queries, warehouse lookups, or enterprise data access.

### What it does now

Right now it returns a stubbed response because real Databricks credentials are not available.

### When it is used

It is used after vector search, when the orchestrator decides structured analysis is the next step.

### Why it matters

This shows that the project is not only about unstructured search.

It also supports the idea of:

- structured enterprise data access
- hybrid workflows
- analytics use cases

### Limitation

It does not yet run a real Databricks query.

That is okay for learning and assignment explanation.

### How to explain it simply

`The Databricks analyst agent is the structured-data specialist. Right now it is a placeholder, but it shows where enterprise data integration would happen.`

### 3.5.5 `finalize_response`

### Why it is used

This function creates the final output for the user.

### What it does

- combines context from earlier steps
- combines Databricks analysis
- combines skill matches
- creates one final answer
- updates memory
- saves session history

### When it is used

It is used at the end of the workflow when all needed information has been collected.

### Why it matters

This is where all agent outputs become one user-facing response.

It also closes the workflow by persisting information.

### How to explain it simply

`finalize_response collects all intermediate results and turns them into the final user response while also saving memory and session data.`

## 3.6 `project/tools.py`

File:
[project/tools.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/tools.py)

### Why this file is used

This file contains helper functions that agents use.

Agents should not directly implement every low-level operation.

Instead, they call tools.

### Main tools

`vector_search`
- searches markdown documents in the knowledge folder

`databricks_query`
- handles Databricks-related structured analysis

`load_skill_library`
- reads skills from text files

### When it is used

Whenever an agent needs one of these capabilities.

### Why it matters

Separating tools from agents improves code organization.

This makes it easier to:

- replace implementations later
- test logic separately
- keep agents cleaner

### How to explain it simply

`tools.py contains reusable helper functions that agents call to perform tasks such as search, data analysis, and skill loading.`

## 3.7 `project/memory_manager.py`

File:
[project/memory_manager.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/memory_manager.py)

### Why this file is used

This file manages long-term and session memory for users.

### What kinds of memory it supports

1. user memory
2. session history

### User memory

This stores persistent notes for a user.

Example:
- user preferences
- recurring interests
- previous request patterns

### Session history

This stores conversation turns inside session files.

Example:
- what the user asked
- what the system answered

### When it is used

- orchestrator reads user memory
- finalizer updates user memory
- finalizer also saves session conversation

### Why it matters

Memory is one of the biggest differences between:

- a simple script
- a real application

It makes the system more personalized and stateful across runs.

### How to explain it simply

`memory_manager.py is responsible for remembering user-related information and storing conversation history for later use.`

## 3.8 `project/guardrails.py`

File:
[project/guardrails.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/guardrails.py)

### Why this file is used

This file adds safety and validation.

### What it does

- checks whether input is empty
- checks whether input is too short
- masks email addresses
- masks phone numbers
- validates whether final output exists

### When it is used

- before the graph runs
- after the graph finishes

### Why it matters

Guardrails are important because:

- not all inputs are good inputs
- sensitive data may need protection
- outputs should be checked for quality/safety

### Why this is useful in a demo

It shows that the system is not only “smart” but also “responsible”.

### How to explain it simply

`guardrails.py protects the workflow by validating inputs and outputs and masking sensitive information.`

## 4. Supporting Folders

## 4.1 `project/knowledge/`

Folder:
[project/knowledge](/Users/nagabhushananarayanareddy/Documents/New%20project/project/knowledge)

### Why it is used

This folder stores source documents that the retrieval system searches.

### What is inside

- assignment requirements
- architecture components

### When it is used

It is used when the vector search agent runs.

### Why it matters

Without documents, retrieval has nothing to search.

This folder gives the project local knowledge.

### How to explain it simply

`The knowledge folder contains the documents that the retrieval agent searches to ground the response.`

## 4.2 `project/skills/`

Folder:
[project/skills](/Users/nagabhushananarayanareddy/Documents/New%20project/project/skills)

### Why it is used

This folder stores reusable capability descriptions.

### What is inside

Examples:

- customer segmentation analysis
- SQL query optimization
- RAG document search
- error diagnosis troubleshooting

### When it is used

The orchestrator reads the skill library to find relevant skills.

### Why it matters

Skills make the system modular and reusable.

Even though they are simple text files now, they represent how reusable procedures can be organized.

### How to explain it simply

`The skills folder stores reusable expertise definitions that the system can refer to while solving tasks.`

## 4.3 `project/memory/`

Folder:
[project/memory](/Users/nagabhushananarayanareddy/Documents/New%20project/project/memory)

### Why it is used

This folder stores per-user data.

### What is inside

For each user:

- `memory.md`
- `sessions/`

### When it is used

Whenever the system reads or writes user history.

### Why it matters

This is how the project achieves user-scoped persistence.

### How to explain it simply

`The memory folder stores separate memory and session history for each user, which helps simulate a real multi-user AI system.`

## 5. How Everything Connects

This is the most important section.

Here is the connection between files:

### Step 1

`main.py` takes input from the user.

### Step 2

`guardrails.py` validates and sanitizes the input.

### Step 3

`main.py` creates the initial state using the structure from `state.py`.

### Step 4

`graph.py` builds the workflow using LangGraph.

### Step 5

`graph.py` calls functions from `agents.py`.

### Step 6

`agents.py` uses helper functions from `tools.py`.

### Step 7

`agents.py` reads and writes memory through `memory_manager.py`.

### Step 8

`finalize_response` produces final output.

### Step 9

`main.py` prints the result and the trace.

This is the complete connection across the project.

## 6. Why Each Component Exists

If someone asks you, “Why did you create so many files?”, use this answer:

- `main.py`: to start the app and handle user interaction
- `config.py`: to centralize settings
- `state.py`: to define shared workflow data
- `graph.py`: to control the execution flow
- `agents.py`: to implement multi-agent logic
- `tools.py`: to separate utility functions from agents
- `memory_manager.py`: to store user memory and sessions
- `guardrails.py`: to validate and sanitize data
- `knowledge/`: to provide retrieval documents
- `skills/`: to provide reusable capabilities
- `memory/`: to persist per-user data

That is the clean architecture reason.

## 7. Why This Is Called a Multi-Agent System

It is called multi-agent because the task is not handled by one block of code alone.

There are distinct roles:

- orchestrator
- vector search specialist
- Databricks analysis specialist
- memory manager
- guardrail layer

Even if all of them are implemented in Python functions right now, architecturally they represent separate agents/components with separate responsibilities.

## 8. Why LangGraph Is Important Here

LangGraph is important because it provides:

- stateful execution
- node-based workflows
- conditional routing
- repeatable agent transitions

Without LangGraph, you could still write `if/else` logic manually.

But LangGraph makes the workflow:

- cleaner
- more explicit
- easier to debug
- easier to scale

## 9. What “When to Use” Means in Practice

You asked specifically to understand why, how, and when each component is used.

Use this quick table mentally:

- `main.py`
  When: when app starts
  Why: to collect input and run the app

- `guardrails.py`
  When: before and after workflow
  Why: to validate and sanitize

- `state.py`
  When: throughout workflow
  Why: to share data between agents

- `graph.py`
  When: after state is created
  Why: to route execution

- `agents.py`
  When: when graph nodes run
  Why: to perform task-specific logic

- `tools.py`
  When: when agents need helper operations
  Why: to keep code modular

- `memory_manager.py`
  When: when reading/writing user history
  Why: to persist user information

- `knowledge/`
  When: during retrieval
  Why: to provide searchable context

- `skills/`
  When: when matching reusable capabilities
  Why: to support modular expertise

## 10. Simple Story You Can Tell Others

If you want to explain the entire project in simple words, say this:

“First, the user enters a prompt. The system validates and cleans the input. Then a shared state object is created. A LangGraph workflow starts and sends the state to the orchestrator agent. The orchestrator checks what information is missing and sends the task to specialized agents. One agent retrieves relevant knowledge from documents, another handles structured analysis. Then a final component combines all outputs into one response and stores user memory and session history. This design makes the system modular, stateful, and closer to a real multi-agent AI application.”

## 11. How You Should Read the Code

Read the project in this order:

1. [project/main.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/main.py)
2. [project/state.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/state.py)
3. [project/graph.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/graph.py)
4. [project/agents.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/agents.py)
5. [project/tools.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/tools.py)
6. [project/memory_manager.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/memory_manager.py)
7. [project/guardrails.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/guardrails.py)
8. [project/config.py](/Users/nagabhushananarayanareddy/Documents/New%20project/project/config.py)

That order is best because:

- first understand the entry point
- then understand the shared state
- then understand the flow
- then understand the worker logic
- then understand helpers and persistence

## 12. Final Memory Tip

Do not try to memorize every line of code.

Instead, remember these three questions for every file:

1. Why does this file exist?
2. When is this file used?
3. What does it give to the system?

If you can answer those three questions, you already understand the architecture well.

## 13. Final Summary

This project is built as a clean multi-agent system with:

- a starting point
- a shared state
- a workflow graph
- specialized agents
- helper tools
- memory
- guardrails
- retrieval knowledge
- reusable skills

Each file has one main responsibility.

That is why the code is split into components.

This is also why the project is easier to explain: every component has a clear purpose.
