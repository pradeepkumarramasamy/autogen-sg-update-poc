# main.py
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from tools import add_ingress_port, commit_template, deploy_stack
import json

# Load your config
with open("config.json") as f:
    config = json.load(f)

llm_config = {
    "config_list": config["config_list"],
    "temperature": 0,
    "tools": [add_ingress_port, commit_template, deploy_stack]
}

# Define agents with tool access
updater = AssistantAgent(
    name="UpdaterAgent",
    llm_config={**llm_config, "tools": [add_ingress_port]},
    system_message="You add ingress rules (TCP ports) to CloudFormation JSON templates."
)

committer = AssistantAgent(
    name="CommitterAgent",
    llm_config={**llm_config, "tools": [commit_template]},
    system_message="You commit and push JSON changes to GitHub using GitPython."
)

deployer = AssistantAgent(
    name="DeployerAgent",
    llm_config={**llm_config, "tools": [deploy_stack]},
    system_message="You deploy CloudFormation templates to AWS using boto3."
)

# Coordinator who can execute code
user_proxy = UserProxyAgent(
    name="Coordinator",
    code_execution_config={"use_docker": False}
)

# Group chat with all agents
groupchat = GroupChat(
    agents=[user_proxy, updater, committer, deployer],
    messages=[],
    max_round=8
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Start the chat with a task prompt
if __name__ == "__main__":
    user_proxy.initiate_chat(
        manager,
        message=(
            "UpdaterAgent: Add ports 8080 and 8443 to `cft/web-sg.json`. "
            "CommitterAgent: Commit with message 'AutoGen function-call commit'. "
            "DeployerAgent: Deploy it as stack `web-sg-stack`."
        )
    )
