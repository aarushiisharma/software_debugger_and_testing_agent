from typing import TypedDict

class SoftwareState(TypedDict):
    user_request:str 
    repository_path:str 

    analysis:str 
    relevant_files:list[str] 

    bug_description:str 
    code_changes:str 

    test_results:str 
    test_passed:bool 

    debug_iterations:int

    final_report:str 