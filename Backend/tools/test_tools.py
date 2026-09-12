# subprocess is a Python standard-library module that allows our application to execute external processes.

import subprocess

def run_tests(repository_path:str):
    """
    Run pytest inside the repository.
    """

    result=subprocess.run(
        ["pytest"],
        cwd=repository_path,
        capture_output=True,
        text=True,
        timeout=60
    )

    return{
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "passed": result.returncode == 0
    }

# def run_python(repository_path:str,file_path:str):
#     """
#     Execute a Python file inside the repository.
#     """

#     result=subprocess.run(
#         ["python",file_path],
#         cwd=repository_path,
#         capture_output=True,
#         text=True,
#         timeout=30
#     )

#     return {
#         "return_code": result.returncode,
#         "stdout": result.stdout,
#         "stderr": result.stderr,
#         "success": result.returncode == 0,
#     }