from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import json

# Load OpenAI config
with open("config.json") as f:
    config = json.load(f)

llm_config = {
    "config_list": config["config_list"],
    "temperature": 0,
    "request_timeout": 60,
}

# Define agents
updater_agent = AssistantAgent(
    name="UpdaterAgent",
    llm_config=llm_config,
    system_message="You update security group JSON templates by adding new ingress rules based on port numbers."
)

committer_agent = AssistantAgent(
    name="CommitterAgent",
    llm_config=llm_config,
    system_message="You commit and push modified CloudFormation templates to GitHub using GitPython."
)

deployer_agent = AssistantAgent(
    name="DeployerAgent",
    llm_config=llm_config,
    system_message="You deploy updated CloudFormation templates to AWS using boto3."
)

user_proxy = UserProxyAgent(
    name="Coordinator",
    code_execution_config={"use_docker": False},
)

# Group chat flow
groupchat = GroupChat(
    agents=[user_proxy, updater_agent, committer_agent, deployer_agent],
    messages=[],
    max_round=6,
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Register the real task
@user_proxy.register_for_execution()
def coordinate_flow():
    from agents.security_group_updater import update_security_group
    from agents.git_committer import commit_and_push_changes
    from agents.deployer import deploy_cft

    TEMPLATE_PORT_MAPPING = {
        "cft/web-sg.json": [8080, 8443],
        "cft/db-sg.json": [3306]
    }

    for template_path, ports in TEMPLATE_PORT_MAPPING.items():
        for port in ports:
            update_security_group(template_path, port)

        commit_and_push_changes(".", f"AutoGen Agent update: opened ports {ports} in {template_path}")
        stack_name = template_path.split("/")[-1].replace(".json", "").replace("-", "_") + "_stack"
        deploy_cft(template_path, stack_name)

    return "✅ All security group templates updated, committed, and deployed."

# Run the agent chat orchestration
user_proxy.initiate_chat(manager, message="Please update all security groups and deploy them to AWS.")
