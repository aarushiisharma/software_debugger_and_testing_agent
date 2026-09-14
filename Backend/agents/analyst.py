# Now the Analyst does this:
# User request
#      ↓
# Analyst LLM
#      ↓
# "I need to inspect the project"
#      ↓
# list_repository_files()
#      ↓
# result → LLM
#      ↓
# "I need to inspect calculator.py"
#      ↓
# read_repository_file()
#      ↓
# result → LLM
#      ↓
# "I should search for add()"
#      ↓
# search_repository_code()
#      ↓
# result → LLM
#      ↓
# final analysis
#      ↓
# relevant_files = ["calculator.py", "tests/test_calculator.py"]

# That is a real tool-using agent.

from langchain_ollama import ChatOllama

from Backend.config.settings import MODEL_NAME

from Backend.tools.agent_tools import(
    list_repository_files,
    read_repository_file,
    search_repository_code,
    inspect_python_project
)

from Backend.agents.agent_runner import run_tool_calling_agent

# Create the language model
llm=ChatOllama(
    model=MODEL_NAME,
    temperature=0,
)

# Tools available to the Code Analyst
analyst_tools=[
    list_repository_files,
    read_repository_file,
    search_repository_code,
    inspect_python_project
]

def code_analyst(state):
    user_request=state["user_request"]
    repository_path=state["repository_path"]

    prompt = f"""
You are the Code Analyst Agent.

Your job is to investigate an existing Python
codebase and identify the cause of a reported
software problem.

You are NOT allowed to modify files.

User request:
{user_request}

Repository:
{repository_path}

Your responsibilities:

1. Inspect the project structure.
2. Find Python files relevant to the problem.
3. Search the code when necessary.
4. Read relevant files.
5. Identify the likely cause of the bug.
6. Provide evidence from the actual code.

Do not guess when you can inspect the code.

Do not implement new features.

Use the available tools whenever necessary.

At the end of your investigation, provide:

ANALYSIS:
Explain the bug and its likely cause.

RELEVANT_FILES:
List the files that the Debugging Agent should inspect.
Use one file path per line.

Do not modify any files.
"""

    analysis=run_tool_calling_agent(
        llm=llm,
        tools=analyst_tools,
        prompt=prompt,
        max_steps=8
    )

    # Extract relevant file paths from the agent response
    relevant_files=extract_relevant_files(analysis)

    # Return state updates to LangGraph
    return {
        "analysis": analysis,
        "relevant_files": relevant_files,
    }

def extract_relevant_files(analysis:str):
    """
    Extract file paths listed under RELEVANT_FILES.
    """

    if "RELEVANT_FILES:" not in analysis:
        return []

    section=analysis.split(
        "RELEVANT_FILES:",
        1
    )[1]

    files=[]

    for line in section.splitlines():
        line=line.strip()

        if not line:
            continue
        # remove common bullet formatting
        line=line.lstrip("-* ")

        if line:
            files.append(line)
    return files