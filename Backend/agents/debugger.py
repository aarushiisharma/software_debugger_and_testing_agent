from langchain_ollama import ChatOllama

from Backend.config.settings import MODEL_NAME

from Backend.tools.agent_tools import(
    read_repository_file,
    search_repository_code,
    update_repository_file
)

from Backend.agents.agent_runner import run_tool_calling_agent

llm=ChatOllama(
    model=MODEL_NAME,
    temperature=0,
)

debugger_tools=[
    read_repository_file,
    update_repository_file,
    search_repository_code
]

def debugger_agent(state):
    user_request = state["user_request"]
    repository_path = state["repository_path"]
    analysis = state["analysis"]
    relevant_files = state["relevant_files"]
    current_iteration = state["debug_iterations"]

    prompt = f"""
You are the Debugging Agent.

Your job is to diagnose and fix an existing
bug in a Python codebase.

You MUST NOT create new features.

User request:
{user_request}

Code Analyst findings:
{analysis}

Relevant files:
{relevant_files}

Debugging iteration:
{current_iteration + 1}

Your responsibilities:

1. Inspect the relevant source code.
2. Confirm the actual bug.
3. Determine why it occurs.
4. Make the smallest appropriate fix.
5. Modify only existing files relevant to the bug.
6. Do not make unrelated changes.
7. Do not create new features.
8. Do not create new files.

Use the available tools to inspect and modify
the repository.

After identifying the correct fix, use
update_repository_file to update the existing
source file.

After making the fix, provide:

BUG:
Explain what the bug was.

CAUSE:
Explain why it happened.

CHANGES:
Explain what you changed.
"""

    result=run_tool_calling_agent(
        llm=llm,
        tools=debugger_tools,
        prompt=prompt,
        max_steps=8
    )

    return{
        "bug_description": result,
        "code_changes": result,
        "debug_iterations": current_iteration + 1
    }