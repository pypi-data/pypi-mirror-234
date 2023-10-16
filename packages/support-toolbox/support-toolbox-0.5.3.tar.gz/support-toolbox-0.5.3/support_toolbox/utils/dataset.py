import requests
import json


def create_dataset(admin_token, org_id, dataset_id, visibility, summary=''):
    create_dataset_url = f"https://api.data.world/v0/datasets/{org_id}"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    payload = {
        "title": dataset_id,
        "summary": summary,
        "visibility": visibility
    }

    body = json.dumps(payload)

    # Create the dataset
    response = requests.post(create_dataset_url, body, headers=header)

    # Verify the creation
    if response.status_code == 200:
        print(f"created dataset: {dataset_id}")
    else:
        print(response.text)
