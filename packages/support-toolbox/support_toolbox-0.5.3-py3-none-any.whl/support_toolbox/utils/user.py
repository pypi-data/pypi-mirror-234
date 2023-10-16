import json
from support_toolbox.utils.helper import PRIVATE_API_URLS
from support_toolbox.utils.org import authorize_access_to_org
import requests

SUPPORT = [
    {
        "agent_id": "jack-compton",
        "display_name": "Jack Compton",
        "email": "jack.compton@data.world",
    },
    {
        "agent_id": "ren-curry",
        "display_name": "Ren Curry",
        "email": "ren.curry@data.world",
    },
    {
        "agent_id": "will-kiyola",
        "display_name": "Will Kiyola",
        "email": "will.kiyola@data.world",
    }
]

ALLOWED_SUPPORT_ROLES = [
    "user",
    "user_api",
    "dwadmin",
    "employee",
    "instance-admin",
    "rate_limit_tier1",
    "support_team",
    "grafo_admin",
    "dwpayments",
    "view-creator"
]


def get_agent_id(admin_token):
    get_user_url = f"{PRIVATE_API_URLS['MT/PI']}/user"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    response = requests.get(get_user_url, cookies=cookies, headers=header)

    # Verify the get
    if response.status_code == 200:
        response_json = response.json()
        agent_id = response_json['agentid']
        return agent_id
    else:
        print(response.text)


def create_user(admin_token, agent_id, display_name, email):
    create_user_url = f"{PRIVATE_API_URLS['MT/PI']}/admin/users"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    data = {
      "agentid": agent_id,
      "displayName": display_name,
      "email": email,
      "visibility": "OPEN"
    }

    body = json.dumps(data)

    response = requests.post(create_user_url, body, cookies=cookies, headers=header)

    # Verify the creation
    if response.status_code == 200:
        print(f"Successfully created: {agent_id}")
    else:
        print(response.text)


def update_user_roles(admin_token, agent_id, allowed_roles):
    update_user_roles_url = f"{PRIVATE_API_URLS['MT/PI']}/admin/{agent_id}/auth"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    data = {
        "allowedRoles": allowed_roles
    }

    body = json.dumps(data)

    response = requests.put(update_user_roles_url, body, cookies=cookies, headers=header)

    # Verify the update
    if response.status_code == 200:
        print(f"Successfully updated: {agent_id} with: {allowed_roles}")
    else:
        print(response.text)


def add_support(admin_token):
    for values in SUPPORT:
        agent_id = values["agent_id"]
        display_name = values["display_name"]
        email = values["email"]

        create_user(admin_token, agent_id, display_name, email)
        update_user_roles(admin_token, agent_id, ALLOWED_SUPPORT_ROLES)
        authorize_access_to_org(admin_token, org_id="datadotworldsupport", party="agent:" + agent_id)
