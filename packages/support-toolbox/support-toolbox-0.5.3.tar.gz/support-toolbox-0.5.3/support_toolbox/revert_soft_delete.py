import json
import requests
from support_toolbox.utils.helper import select_resource, select_api_url


# Revert soft delete for a resource
def revert_soft_delete(admin_token, org, iri, resource_type, customer_url):
    url = f"{customer_url}/editActivities/{org}/ddw-catalogs"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    resource_data = {
        "changeMessage": "Revert deleted resources",
        "activities": [{
            "type": "RevertSoftDelete",
            "entityType": resource_type,
            "target": iri
        }, {
            "type": "RevertSoftDelete",
            "entityType": resource_type,
            "target": iri
        }]
    }

    body = json.dumps(resource_data)
    response = requests.post(url, body, cookies=cookies, headers=header)

    # Verify the revert
    if response.status_code == 200:
        print(f"Successfully reverted soft delete for: {iri}")
    else:
        print(response.text)


def run():
    api_url = select_api_url("private")
    admin_token = input("Enter your active admin token for the selected customer: ")
    org = input("Enter the org ID where the resource is located: ")
    iri = input("Enter the resource IRI: ")
    resource_type = select_resource()
    revert_soft_delete(admin_token, org, iri, resource_type, api_url)
