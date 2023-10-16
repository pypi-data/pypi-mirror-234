import json
import requests
from datetime import datetime
from support_toolbox.utils.helper import PRIVATE_API_URLS

# Add ORG Level Default Entitlements here
ORG_DEFAULT_ENTITLEMENTS = {
    "Organization Member Seat Count - Unlimited": "2c20846c-57b2-491f-bbd7-1f32bf0dec2c"
}

# Add USER Level Default Entitlements here
USER_DEFAULT_ENTITLEMENTS = {
    "No Personal Datasets": "d9cdbf86-06c4-4e39-8d15-2874e50d2fae"
}


def update_org_entitlements(admin_token, org_id, product_id, order, source, name):
    update_entitlements_url = f"{PRIVATE_API_URLS['MT/PI']}/entitlements"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    # Format the datetime as a string in the expected format
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    data = {
      "agentid": org_id,
      "entitlementItems": [
        {
          "productid": product_id,
          "quantity": "1"
        }
      ],
      "order": order,
      "source": source,
      "startDate": timestamp
    }

    body = json.dumps(data)
    response = requests.post(update_entitlements_url, body, cookies=cookies, headers=header)

    # Verify the update
    if response.status_code == 200:
        print(f"Successfully updated {org_id} with {name}")
    else:
        print(response.text)


def get_entitlements(admin_token, org_id):
    get_entitlements_url = f"{PRIVATE_API_URLS['MT/PI']}/entitlements/{org_id}"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    response = requests.get(get_entitlements_url, cookies=cookies, headers=header)

    # Verify the response
    if response.status_code == 200:
        response_json = response.json()
        return response_json['records'][0]['source']
    else:
        print(response.text)


def get_default_values(admin_token, agent_type):
    get_offering_url = f"{PRIVATE_API_URLS['MT/PI']}/offerings/agentTypes/{agent_type}"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    response = requests.get(get_offering_url, cookies=cookies, headers=header)

    # Verify the response
    if response.status_code == 200:
        response_json = response.json()

        result = {
            'agent_type': response_json['records'][0]['agentType'],
            'offering_slug': response_json['records'][0]['offeringSlug'],
            'offering_id': response_json['records'][0]['offeringid'],
            'product_ids': response_json['records'][0]['productids']
        }

        return result
    else:
        print(response.text)


# Take an agentType as parameter to update either org or user default plans
def update_default_plan(admin_token, offering_id, agent_type, offering_slug, product_ids):
    update_default_plan_url = f"{PRIVATE_API_URLS['MT/PI']}/offerings/{offering_id}"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    # Format the datetime as a string in the expected format
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    data = {
        "agentType": agent_type,
        "defaultOffering": True,
        "offeringSlug": offering_slug,
        "offeringid": offering_id,
        "pricingModel": {},
        "productids": product_ids,
        "requiresPayment": False,
        "startDate": timestamp
    }

    body = json.dumps(data)
    response = requests.put(update_default_plan_url, body, cookies=cookies, headers=header)

    # Verify the update
    if response.status_code == 200:
        if agent_type == 'organization':
            for name in ORG_DEFAULT_ENTITLEMENTS:
                print(f"Successfully updated {agent_type} Default Plan with: {name}")
        elif agent_type == 'user':
            for name in USER_DEFAULT_ENTITLEMENTS:
                print(f"Successfully updated {agent_type} Default Plan with: {name}")
    else:
        print(response.text)
