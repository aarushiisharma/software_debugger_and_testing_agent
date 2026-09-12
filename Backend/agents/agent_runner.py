import json

from langchain_core.messages import HumanMessage,ToolMessage

def run_tool_calling_agent(llm,tools,prompt:str,max_steps:int=8):
    """
    Run an LLM agent that can call tools.

    The LLM decides which tool to use.
    The Python application executes the tool.
    The tool result is sent back to the LLM.
    This continues until the LLM gives a final answer.
    """

    tool_map={
        tool.name:tool for tool in tools
    }
    model=llm.bind_tools(tools)

    messages=[
        HumanMessage(content=prompt)
    ]

    for _ in range(max_steps):
        response=model.invoke(messages)

        messages.append(response)

        # No tool call means the agent has produced its final response.
        if not response.tool_calls:
            return response.content

        # Execute every requested tool
        for tool_call in response.tool_calls:
            tool_name=tool_call["name"]
            tool_args=tool_call["args"]
            tool_call_id=tool_call["id"]

            tool=tool_map.get(tool_name)

            if tool is None:
                result=f"Unknown tool : {tool_name}"
            else:
                try:
                    result=tool.invoke(tool_args)
                except Exception as error:
                    result=f"Tool execution error : {error}"
            # Convert dictionaries/lists into JSON strings
            if not isinstance(result,str):
                result=json.dumps(
                    result,
                    default=str
                )
            messages.append(
                ToolMessage(
                    content=result,
                    tool_call_id=tool_call_id
                )
            )
    return "Agent stopped because maximum tool-calling steps were reached."       