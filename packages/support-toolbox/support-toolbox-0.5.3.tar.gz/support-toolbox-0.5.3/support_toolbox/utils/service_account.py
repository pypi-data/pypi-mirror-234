import requests
import json
from support_toolbox.utils.helper import PRIVATE_API_URLS

# Create Service Account payloads
SERVICE_ACCOUNTS = [
    {
        "desiredUsername": "ctk",
        "displayName": "DDW Catalog Toolkit Service"
    },
    {
        "desiredUsername": "ddwmetrics",
        "displayName": "DDW Platform Metrics Service"
    }
]

CIRCLECI_PROJECTS = ["catalog-config", "mca"]


def create_env_variable(circleci_project, name, value, circleci_api_token):
    url = f"https://circleci.com/api/v2/project/github/datadotworld/{circleci_project}/envvar"

    headers = {
        "Circle-Token": circleci_api_token
    }

    payload = {
        "name": name,
        "value": value
    }

    response = requests.post(url, payload, headers=headers)

    if response.status_code == 201:
        print(f"Added '{name}' to the '{circleci_project}' project environment variables in CircleCI ")
    else:
        print(f"Error: Unable to create environment variables. Status Code: {response.status_code}")


def create_service_account(api_token, payload):
    create_service_account_url = f"{PRIVATE_API_URLS['MT/PI']}/serviceaccount/datadotworldsupport"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    cookies = {
        'adminToken': api_token
    }

    body = json.dumps(payload)

    # Create the service account
    response = requests.post(create_service_account_url, body, cookies=cookies, headers=header)

    # Verify the creation
    if response.status_code == 200:
        response_json = response.json()

        service_account = response_json['serviceAccountUsername']
        service_account_token = response_json['token']
        print(f"created service account: {service_account}")
        print(f"token: {service_account_token}")
        return service_account_token
    else:
        print(response.text)

