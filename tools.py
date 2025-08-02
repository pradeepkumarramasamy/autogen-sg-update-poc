# tools.py
from autogen_core.tools import FunctionTool
from git import Repo

# Assuming these imports are correct and represent your actual functions
from agents.security_group_updater import update_security_group
from agents.git_committer import commit_and_push_changes
from agents.deployer import deploy_cft

def add_ingress_port(template_path: str, port: int) -> str:
    update_security_group(template_path, port)
    return f"✅ Port {port} added to {template_path}"

def commit_template(repo_path: str, message: str) -> str:
    repo = Repo(repo_path, search_parent_directories=True)
    return commit_and_push_changes(repo_path, message)

def deploy_stack(template_path: str, stack_name: str) -> str:
    deploy_cft(template_path, stack_name)
    return f"✅ Stack '{stack_name}' deployed using {template_path}"

# Create instances of FunctionTool for each function to be used as a tool
add_ingress_port_tool = FunctionTool(
    add_ingress_port,
    description="Adds a TCP ingress rule to a CloudFormation JSON template."
)

commit_template_tool = FunctionTool(
    commit_template,
    description="Commits and pushes changes to a Git repository. "
                "Takes the path to the repository folder (not a file) and a commit message."
)

deploy_stack_tool = FunctionTool(
    deploy_stack,
    description="Deploys a CloudFormation stack using the provided JSON template."
)

# You can then expose these `_tool` variables for use in your agents,
# or register them with the agents using `register_for_llm` and `register_for_execution`,
# or using the convenience function `autogen.register_function`.
