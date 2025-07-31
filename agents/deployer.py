import boto3
from botocore.exceptions import ClientError
import os

def deploy_cft(template_path: str, stack_name: str, region: str = "us-east-1") -> None:
    if not os.path.exists(template_path):
        print(f"❌ Template file not found: {template_path}")
        return

    with open(template_path, 'r') as file:
        template_body = file.read()

    cf = boto3.client('cloudformation', region_name=region)

    try:
        response = cf.update_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_NAMED_IAM']
        )
        print(f"🔄 Updating stack: {stack_name}")
        waiter = cf.get_waiter('stack_update_complete')
    except ClientError as e:
        if "does not exist" in str(e):
            response = cf.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Capabilities=['CAPABILITY_NAMED_IAM']
            )
            print(f"🆕 Creating stack: {stack_name}")
            waiter = cf.get_waiter('stack_create_complete')
        elif "No updates are to be performed" in str(e):
            print(f"✅ Stack {stack_name} already up to date.")
            return
        else:
            raise e

    print("⏳ Waiting for stack operation to complete...")
    waiter.wait(StackName=stack_name)
    print(f"✅ Stack {stack_name} deployed successfully.")
