from autogen_core.tools import FunctionTool
# The 'Tool' base class might not be necessary for simple function tools. 
# Also, the @tool decorator is not directly supported in this way in autogen_core.tools.

def greet(name: str) -> str:
    """Greets a user by name.
    Args:
        name (str): The name of the user to greet.
    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Create an instance of FunctionTool to wrap the 'greet' function
    greet_tool = FunctionTool(
        greet, 
        description="Greets a user by name."
    )

    # To run the tool directly outside of an agent conversation, 
    # you would typically call its underlying function or use a specific method if available. 
    # For a simple FunctionTool, directly calling the wrapped function is often sufficient for testing.
    print(greet("Pradeep"))

    # If you were to integrate this into an agent conversation, 
    # the agent would handle the execution of the tool, potentially through a method like 'run_json' 
    # if the tool was set up to handle JSON inputs.
