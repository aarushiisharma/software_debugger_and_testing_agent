from Backend.tools.agent_tools import execute_tests

def testing_agent(state):
    """
    Run the project's automated tests.
    """

    repository_path=state["repository_path"]
    result=execute_tests.invoke({
        "repository_path":repository_path
    })

    test_output=(
        result["stdout"]+"\n"+result["stderr"]
    )

    return {
        "test_results":test_output,
        "test_passed":result["passed"]
    }