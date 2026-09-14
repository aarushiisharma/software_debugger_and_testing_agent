from langchain_ollama import ChatOllama

from Backend.config.settings import MODEL_NAME

llm=ChatOllama(
    model=MODEL_NAME,
    temperature=0,
)

def supervisor_agent(state):
    user_request = state["user_request"]

    prompt = f"""
You are the Supervisor Agent for a software
debugging and testing system.

The system handles ONLY:

- code analysis
- debugging existing code
- testing

It does NOT implement new features.

User request:
{user_request}

Your job is to understand the user's request
and provide a high-level plan for the specialist
agents.

Available specialists:

Code Analyst:
- investigates the repository
- searches code
- reads files
- identifies the likely cause

Debugging Agent:
- diagnoses the confirmed bug
- modifies existing code
- fixes the bug

Testing Agent:
- runs automated tests
- determines whether the fix works

Explain which specialist should handle the
problem first and what they should focus on.

Do not modify any files.
"""
    
    response = llm.invoke(prompt)

    return {
        "analysis": response.content,
    }