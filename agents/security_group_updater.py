import json
import os

def update_security_group(template_path: str, port: int) -> None:
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return

    with open(template_path, 'r') as f:
        data = json.load(f)

    # Assume only one SG in Resources
    sg_resource = list(data['Resources'].values())[0]
    ingress_rules = sg_resource['Properties'].get("SecurityGroupIngress", [])

    new_rule = {
        "IpProtocol": "tcp",
        "FromPort": port,
        "ToPort": port,
        "CidrIp": "0.0.0.0/0"
    }

    if new_rule in ingress_rules:
        print(f"⚠️ Port {port} already exists in {template_path}.")
        return

    ingress_rules.append(new_rule)
    sg_resource['Properties']["SecurityGroupIngress"] = ingress_rules

    with open(template_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Port {port} added to {template_path}")
