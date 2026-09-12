from Backend.tools.file_tools import get_repository_path

def search_code(repository_path:str,search_term:str):
    """
    Search for a term inside Python files.
    """

    repository=get_repository_path(repository_path)

    matches=[]

    # search only python files
    for file_path in repository.rglob("*.py"):
        try:
            content=file_path.read_text(
                encoding="utf-8"
            )
        except UnicodeDecodeError:
            continue
        if search_term.lower() in content.lower():
            relative_path=(
                file_path.relative_to
                (repository)
            )
            matches.append(
                str(relative_path)
            )
    return matches

def inspect_project(repository_path:str):
    """
    Inspect the basic structure of a Python project.
    """

    repository=get_repository_path(repository_path)

    python_files=list(repository.rglob("*.py"))

    test_files=[]

    for path in python_files:
        if "test" in path.name.lower():
            test_files.append(path)

    return {
        "repository": str(repository),
        "python_files": len(python_files),
        "test_files": len(test_files),
        "has_tests": len(test_files) > 0
    }