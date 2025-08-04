# tools.py
import os
import re
from autogen_core.tools import FunctionTool
from git import Repo

# Assuming these imports are correct and represent your actual functions
from agents.security_group_updater import update_security_group
from agents.git_committer import commit_and_push_changes
from agents.deployer import deploy_cft

def add_ingress_port(template_path: str, port: int) -> str:
    update_security_group(template_path, port)
    return f"✅ Port {port} added to {template_path}"

'''def commit_template(repo_path: str, message: str) -> str:
    repo = Repo(repo_path, search_parent_directories=True)
    return commit_and_push_changes(repo_path, message)

def deploy_stack(template_path: str, stack_name: str) -> str:
    deploy_cft(template_path, stack_name)
    return f"✅ Stack '{stack_name}' deployed using {template_path}"'''

def commit_template(repo_path: str, message: str, stack_name: str | None = None) -> str:
    repo = Repo(repo_path, search_parent_directories=True)
    commit_result = commit_and_push_changes(repo_path, message)

    '''# 🚀 Trigger deployment right after commit
    template_path = f"{repo_path}/web-sg.json"
    stack_name = "web-sg-stack"'''
   # Infer template file from message or fallback
    matches = re.findall(r'cft/([\w\-]+\.json)', message)
    template_file = matches[0] if matches else "web-sg.json"
    template_path = f"{repo_path}/{template_file}"

    # Infer stack name if not provided
    if not stack_name:
        base = template_file.split(".")[0].replace("_", "-")
        stack_name = base if base.endswith("-stack") else f"{base}-stack"
    
    deploy_cft(template_path, stack_name or "default-stack-name")
    return f"{commit_result}\n🚀 Deployed stack '{stack_name}' with updated template."


# Create instances of FunctionTool for each function to be used as a tool
add_ingress_port_tool = FunctionTool(
    add_ingress_port,
    description="Adds a TCP ingress rule to a CloudFormation JSON template."
)

commit_template_tool = FunctionTool(
    commit_template,
    description=(
        "Commits and pushes changes to a Git repository and deploys the CloudFormation stack. "
        "Provide: repo path, commit message, and optionally stack name. "
        "If stack name is omitted, it will be inferred from the template file."
    )
)

'''deploy_stack_tool = FunctionTool(
    deploy_stack,
    description="Deploys a CloudFormation stack using the provided JSON template."
)'''

# You can then expose these `_tool` variables for use in your agents,
# or register them with the agents using `register_for_llm` and `register_for_execution`,
# or using the convenience function `autogen.register_function`.
