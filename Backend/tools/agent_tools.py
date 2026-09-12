# LangChain's @tool converts the Python function into a tool that an LLM can understand and request.

# So agent_tools.py takes your existing functions and wraps them.

from langchain_core.tools import tool

from Backend.tools.file_tools import list_files,read_file,write_file
from Backend.tools.code_tools import search_code,inspect_project
from Backend.tools.test_tools import run_tests

@tool
def list_repository_files(repository_path:str):
    """List all files inside the Python repository."""
    return list_files(repository_path)

@tool
def read_repository_file(repository_path:str,file_path:str):
    """Read the contents of a file inside the repository."""
    return read_file(repository_path, file_path)

@tool
def update_repository_file(repository_path:str,file_path:str,content:str):
    """
    Update an existing file inside the repository.
    Use this only to fix an identified bug.
    """

    return write_file(repository_path,file_path,content)

@tool
def search_repository_code(repository_path:str,search_term:str):
    """Search Python source files for a keyword or piece of code."""
    return search_code(repository_path, search_term)

@tool
def inspect_python_project(repository_path: str):
    """Inspect the structure of a Python project."""
    return inspect_project(repository_path)


@tool
def execute_tests(repository_path: str):
    """Run the project's pytest test suite."""
    return run_tests(repository_path)
