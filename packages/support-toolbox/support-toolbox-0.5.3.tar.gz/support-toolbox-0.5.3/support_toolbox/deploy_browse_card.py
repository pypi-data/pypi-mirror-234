import requests
import json
from support_toolbox.utils.dataset import create_dataset

VAlIDATION_QUERIES = [
    {
        "name": "Is SHACL Passing",
        "content": """PREFIX sh:  <http://www.w3.org/ns/shacl#> 
SELECT ?conforms WHERE {
        ?s a sh:ValidationReport .
        ?s sh:conforms ?conforms
}""",
        "language": "SPARQL",
        "published": True
    },
    {
        "name": "SHACL Validation Report",
        "content": """PREFIX sh: <http://www.w3.org/ns/shacl#>

SELECT ?violatingNode ?violatingPredicate ?message
WHERE {
    ?s         sh:result        ?violation.
    ?violation sh:focusNode     ?violatingNode.
    ?violation sh:resultPath    ?violatingPredicate.
    ?violation sh:resultMessage ?message.
}""",
        "language": "SPARQL",
        "published": True
    }
]


def create_saved_query(api_token, q, owner, dataset_id):
    create_saved_query_url = f"https://api.data.world/v0/datasets/{owner}/{dataset_id}/queries"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    body = json.dumps(q)

    # Create the query
    response = requests.post(create_saved_query_url, body, headers=header)

    # Verify the creation
    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
    else:
        print(response.text)


def deploy_browse_card(api_token, selection):
    org_id = 'ddw'
    dataset_id = 'ddw-instance-profile'

    if selection == 'y':
        org_id = input("Enter the org_id to deploy a browse card to: ")
        dataset_id = "ddw-profile-configuration"

    create_dataset(api_token, org_id, dataset_id, "DISCOVERABLE")

    for q in VAlIDATION_QUERIES:
        create_saved_query(api_token, q, org_id, dataset_id)


def run():
    api_token = input("Enter your API Token for the site you are deploying a browse card to: ")

    while True:
        selection = input("Is this an org level browse card? (y/n): ")

        if selection == 'y' or selection == 'n':
            deploy_browse_card(api_token, selection)
            break

        else:
            print("Enter a valid option: 'y'/'n'")
