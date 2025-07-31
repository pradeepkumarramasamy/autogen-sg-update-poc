from agents.security_group_updater import update_security_group
from agents.git_committer import commit_and_push_changes
from agents.deployer import deploy_cft

TEMPLATE_PORT_MAPPING = {
    "cft/web-sg.json": [8080, 8443],
    "cft/db-sg.json": [3306]
}

def run_full_flow():
    for template_path, ports in TEMPLATE_PORT_MAPPING.items():
        stack_name = template_path.split("/")[-1].replace(".json", "").replace("-", "_") + "_stack"

        for port in ports:
            update_security_group(template_path, port)

        commit_and_push_changes(".", f"AutoGen: Updated ports {ports} in {template_path}")
        deploy_cft(template_path, stack_name)

if __name__ == "__main__":
    run_full_flow()
