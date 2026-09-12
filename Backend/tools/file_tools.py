from pathlib import Path

def get_repository_path(repository_path:str):
    """
    Return the resolved repository path.
    """
    repository=Path(repository_path).resolve()

    if not repository.exists():
        raise FileNotFoundError(
            f"Repository not found : {repository_path}"
        )
    if not repository.is_dir():
        raise ValueError(
            f"Repository path is not a directory : {repository_path}"
        )
    return repository

def list_files(repository_path:str):
    """
    List all files inside the repository.
    """

    repository=get_repository_path(repository_path)

    files=[]

    for file_path in repository.rglob("*"):
        if file_path.is_file():
            files.append(
                str(file_path.relative_to(repository))
            )
    return files

def read_file(repository_path:str,file_path:str):
    """
    Read a file from inside the repository.
    """

    repository=get_repository_path(repository_path)

    target_file=(repository/file_path).resolve()

    # Security check: prevent access outside repository
    if not target_file.is_relative_to(repository):
        raise PermissionError(
            "Cannot access files outside the repository"
        )
    if not target_file.exists():
        raise FileNotFoundError(
            f"File not found : {file_path}"
        )
    if not target_file.is_file():
        raise ValueError(
            f"Path is not a file : {file_path}"
        )
    return target_file.read_text(
        encoding="utf-8"
    )

def write_file(repository_path:str,file_path:str,content:str):
    """
    Write new content to an existing file inside the repository.
    """

    repository=get_repository_path(repository_path)

    target_file=(repository/file_path).resolve()

    # Prevent access outside the repository
    if not target_file.is_relative_to(repository):
        raise PermissionError(
            "Cannot access files outside the repository"
        )
    # Only modify existing files
    if not target_file.exists():
        raise FileNotFoundError(
            f"File not found : {file_path}"
        )
    if not target_file.is_file():
        raise ValueError(
            f"Path is not a file : {file_path}"
        )
    target_file.write_text(
        content,
        encoding="utf-8"
    )
    return f"Successfully updated {file_path}"