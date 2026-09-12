from fastapi import FastAPI
from pydantic import BaseModel

from Backend.graph.workflow import build_workflow

app=FastAPI(
    title="Multi-Agent Software Debugging & Testing System"
)

# Build the LangGraph workflow once when the application starts
workflow=build_workflow()

class DebugRequest(BaseModel):
    user_request:str 
    repository_path:str 

@app.get("/")
def root():
    return {
        "message": "Multi-Agent Debugging System is running"
    }

# @app.post("/debug")
# def debug_project(request:DebugRequest):
#     initial_state={
#         "user_request": request.user_request,
#         "repository_path": request.repository_path,
#         "analysis": "",
#         "relevant_files": [],
#         "bug_description": "",
#         "code_changes": "",
#         "test_results": "",
#         "tests_passed": False,
#         "debug_iterations": 0,
#         "final_report": ""
#     }

#     result=workflow.invoke(initial_state)
#     return result

@app.post("/debug")
def debug_project(request: DebugRequest):

    print("\n==============================", flush=True)
    print("DEBUG REQUEST RECEIVED", flush=True)
    print("==============================", flush=True)

    print(
        "User request:",
        request.user_request,
        flush=True
    )

    print(
        "Repository:",
        request.repository_path,
        flush=True
    )

    initial_state = {
        "user_request": request.user_request,
        "repository_path": request.repository_path,
        "analysis": "",
        "relevant_files": [],
        "bug_description": "",
        "code_changes": "",
        "test_results": "",
        "tests_passed": False,
        "debug_iterations": 0,
        "final_report": "",
    }

    print("Starting workflow...", flush=True)

    try:
        result = workflow.invoke(initial_state)

        print(
            "Workflow completed successfully.",
            flush=True
        )

        return result

    except Exception as error:

        print(
            "\n!!! WORKFLOW ERROR !!!",
            flush=True
        )

        print(
            "ERROR TYPE:",
            type(error).__name__,
            flush=True
        )

        print(
            "ERROR:",
            str(error),
            flush=True
        )

        print(
            "========================\n",
            flush=True
        )

        raise