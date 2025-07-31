from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import json

# Load OpenAI API key and config
with open("config.json") as f:
    config = json.load(f)

llm_config = {
    "config_list": config["config_list"],
    "temperature": 0
}

# Define agents
updater_agent = AssistantAgent(
    name="UpdaterAgent",
    llm_config=llm_config,
    system_message="You update CloudFormation JSON templates to add new ingress rules."
)

committer_agent = AssistantAgent(
    name="CommitterAgent",
    llm_config=llm_config,
    system_message="You commit and push updated CloudFormation templates using GitPython."
)

deployer_agent = AssistantAgent(
    name="DeployerAgent",
    llm_config=llm_config,
    system_message="You deploy CloudFormation stacks using boto3."
)

# UserProxyAgent is the only one that can actually execute code
user_proxy = UserProxyAgent(
    name="Coordinator",
    code_execution_config={"use_docker": False}
)

# Group chat setup
groupchat = GroupChat(
    agents=[user_proxy, updater_agent, committer_agent, deployer_agent],
    messages=[],
    max_round=5,
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# ✅ Actual work: update + git commit + deploy
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
        stack_name = template_path.split("/")[-1].replace(".json", "").replace("_", "-") + "-stack"
        deploy_cft(template_path, stack_name)

    return "✅ All security group templates updated, committed, and deployed."

# 🔁 Start the agent chat and execute the registered flow
# Force execution directly
if __name__ == "__main__":
    coordinate_flow()

