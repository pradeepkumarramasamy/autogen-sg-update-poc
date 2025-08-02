import asyncio
import json
from autogen_core.models import UserMessage
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# ✅ Your tools (FunctionTool wrapped functions)
from tools import (
    add_ingress_port_tool,
    commit_template_tool,
    #deploy_stack_tool,
)

# ✅ Load OpenAI model config
with open("config.json") as f:
    config_data = json.load(f)

model = config_data["config_list"][0]["model"]
api_key = config_data["config_list"][0]["api_key"]

# ✅ Create model client
model_client = OpenAIChatCompletionClient(
    model=model,
    api_key=api_key,
    temperature=0,
)

# ✅ Create assistant agent and register tools
assistant = AssistantAgent(
    name="DeployerAgent",
    model_client=model_client,
    system_message=(
        "You update CloudFormation templates by adding ingress rules, "
        "commit changes to GitHub, and deploy the updated stack to AWS. "
        "Use the available tools to perform these actions."
    ),
    tools=[
        add_ingress_port_tool,
        commit_template_tool,
       # deploy_stack_tool,
    ]
)

# ✅ Construct user message manually
message = UserMessage(
    content="Please add port 1234 to cft/web-sg.json, commit it with the message "
            "'AutoGen update: open port 5432', and deploy to the stack named 'web_sg_stack'.",
    source="user"
)


# ✅ Run assistant agent to process the message and invoke tools
async def main():
    response = await assistant.run(
        task="Please add port 3 to cft/web-sg.json, commit it with the message 'AutoGen update: open port 2', and make sure to deploy the stack named 'web_sg_stack' using the updated template."
    )
    print("--- Assistant Response ---")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
