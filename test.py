from autogen.tools import tool

@tool  # type: ignore
def greet(name: str) -> str:
    """Greets a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet.run("Pradeep"))
