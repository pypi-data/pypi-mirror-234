import requests
import json
import subprocess
import os

INTEGRATIONS = [
    "athena", "azure-synapse", "bigquery", "denodo",
    "ibm-db2", "infor-ion", "java-jdbc", "microsoft-sql-server",
    "mysql", "oracle-database", "postgresql",
    "python", "redshift", "snowflake"
]


def push_integration(integration):
    # Append the desired directory to the PATH temporarily for the subprocess call
    os.environ['PATH'] = os.pathsep.join([os.environ['PATH'], os.path.expanduser('~/.dw/cli/bin')])

    # Determine the path to Java 11 and set JAVA_HOME
    java_home_command = '/usr/libexec/java_home -v 11'
    java_home_output = subprocess.check_output(java_home_command, shell=True, text=True).strip()
    os.environ['JAVA_HOME'] = java_home_output

    command = f"bin/apply {integration}.template"

    directory_path = os.path.expanduser("~/integration-templates")

    # Execute the terminal command in the specified directory
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            cwd=directory_path)

    # Check the result
    if result.returncode == 0:
        print("Command executed successfully:")
        print(result.stdout)
    else:
        print("Command failed:")
        print(result.stderr)


def add_discoverable_to_integration(org, dataset_id, api_token):
    update_dataset = f"https://api.data.world/v0/datasets/{org}/{dataset_id}"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    payload = {
        "visibility": "DISCOVERABLE"
    }
    body = json.dumps(payload)

    # Update a specific dataset
    response = requests.patch(update_dataset, body, headers=header)

    # Verify the update
    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
    else:
        print(response.text)


def deploy_integrations(api_token, selection):
    os.environ["DW_AUTH_TOKEN"] = api_token

    if selection == '1':
        # Deploy all specific integrations in the INTEGRATIONS list
        for integration_name in INTEGRATIONS:
            push_integration(integration_name)
            add_discoverable_to_integration("datadotworld-apps", integration_name, api_token)
    elif selection == '2':
        # Deploy a specific integration
        integration_name = input("Enter the name of the integration you want to deploy: ")
        push_integration(integration_name)
        add_discoverable_to_integration("datadotworld-apps", integration_name, api_token)


def run():
    api_token = input("Enter your API Token for the site you are deploying integrations to: ")

    # Display integration list
    for integration in INTEGRATIONS:
        print(integration)

    selection = input("Enter '1' to deploy the default list of integrations, or '2' to specify an integration outside the list: ")

    if selection == '1' or selection == '2':
        deploy_integrations(api_token, selection)
    else:
        print("Invalid selection. Please enter '1' to deploy all listed integrations or '2' to deploy a specific integration.")
