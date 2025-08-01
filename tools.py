# tools.py
from autogen import tool
from agents.security_group_updater import update_security_group
from agents.git_committer import commit_and_push_changes
from agents.deployer import deploy_cft

@tool
def add_ingress_port(template_path: str, port: int):
    """Add a TCP ingress rule to the given CloudFormation JSON template."""
    update_security_group(template_path, port)

@tool
def commit_template(repo_path: str, message: str):
    """Commit and push changes to a GitHub repository."""
    commit_and_push_changes(repo_path, message)

@tool
def deploy_stack(template_path: str, stack_name: str):
    """Deploy a CloudFormation stack using the provided JSON template."""
    deploy_cft(template_path, stack_name)
