from langgraph.graph import StateGraph,START,END

from Backend.graph.state import SoftwareState

from Backend.agents.supervisor import supervisor_agent
from Backend.agents.analyst import code_analyst
from Backend.agents.debugger import debugger_agent
from Backend.agents.tester import testing_agent

def should_continue(state:SoftwareState):
    """
    Decide whether the workflow should finish
    or send the project back to the Debugging Agent.
    """

    # If all tests passed, debugging is complete.
    if state["test_passed"]:
        return "end"

    # Prevent the system from getting stuck in an infinite debugging loop.
    if state["debug_iterations"]>=3:
        return "end"
    
    # Tests failed, so Debugger should try again.
    return "debug"

def build_workflow():
    """
    Build and compile the software debugging workflow.
    """

    graph=StateGraph(SoftwareState)

    # Add agents as graph nodes
    graph.add_node("supervisor",supervisor_agent)
    graph.add_node("analyst",code_analyst)
    graph.add_node("debugger",debugger_agent)
    graph.add_node("tester",testing_agent)

    # Starting point
    graph.add_edge(START,"supervisor")

    # Supervisor → Analyst
    graph.add_edge("supervisor","analyst")

    # Analyst → Debugger
    graph.add_edge("analyst", "debugger")

    # Debugger → Tester
    graph.add_edge("debugger", "tester")

    # Tester decides what happens next
    graph.add_conditional_edges(
        "tester",
        should_continue,
        {
            "debug": "debugger",
            "end": END,
        },
    )

    return graph.compile()