import configparser
import requests
import os
from jira import JIRA

# Get the path to the user's home directory
user_home = os.path.expanduser("~")

# Construct the full path to the configuration file
tokens_file_path = os.path.join(user_home, ".tokens.ini")

# Initialize the configparser and read the tokens configuration file
config = configparser.ConfigParser()
config.read(tokens_file_path)

# Read tokens/variables for the delete_users tool
dw_api_token = config['delete_users']['DWSUPPORT_API_TOKEN']
jira_api_token = config['delete_users']['JIRA_API_TOKEN']
jira_username = config['delete_users']['JIRA_USERNAME']

# Swagger API Endpoints
get_agent_id_endpoint = "https://k2xz8y420efx4a3j.data.world/api/v0/users"
delete_agent_id_endpoint = "https://k2xz8y420efx4a3j.data.world/api/v0/admin/users/"

# Public API Endpoints
execute_saved_query_endpoint = "https://api.data.world/v0/queries/b06e6e0e-27ba-400a-8ace-3b0982c7cbf1/results"

# List of emails to delete
emails_to_delete = []

# Dictionary of key 'emails' with the associated value 'issue_key' used when interacting with the JIRA API
tickets_to_close = {}


def close_ticket(issue_key):
    # Initialize JIRA API
    jira = JIRA(server='https://dataworld.atlassian.net', basic_auth=(jira_username, jira_api_token))
    issue = jira.issue(issue_key)

    # Adding a comment
    jira.add_comment(issue,
                     'Hi,\n\nThis message is to confirm that we have deleted your data.world account.\n\nKind regards,\nThe data.world team')

    # Removing 'Customer Responded'
    issue.update(fields={'customfield_11095': None})

    # Transition to 'Solved' id = '201'
    jira.transition_issue(issue, transition='201')


def get_deletion_requests():
    print("Getting all tickets where the customer has confirmed to delete their account...")

    header = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {dw_api_token}'
    }

    response = requests.get(execute_saved_query_endpoint, headers=header)

    # Verify that there are tickets ready for delete
    if response.status_code == 200:
        response_json = response.json()

        for i in range(len(response_json)):
            issue_key = response_json[i]['t1.issue_key']
            reporter = response_json[i]['reporter']

            print(issue_key, reporter)
            emails_to_delete.append(reporter)
            tickets_to_close[f'{reporter}'] = issue_key

    else:
        print("\nThere are no users to delete!")
        return False

    return True


def delete_agent_id(agent_id, email, admin_token):
    header = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    body = {
        'agentid': agent_id
    }

    response = requests.delete(delete_agent_id_endpoint + agent_id, params=body, headers=header, cookies=cookies)

    if response.status_code == 200:
        print(f"Deleted user: {agent_id}")

        close_ticket(tickets_to_close[f'{email}'])
        print(f"Closing ticket: {tickets_to_close[f'{email}']}")

        return
    else:
        print(response.text)


def get_agent_id(email, admin_token):
    header = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {admin_token}'
    }

    cookies = {
        'adminToken': admin_token
    }

    body = {
        'email': email
    }

    response = requests.get(get_agent_id_endpoint, params=body, headers=header, cookies=cookies)

    if response.status_code == 200:
        agent_id = response.json()['agentid']
        print(f"Found: {agent_id}")

        return agent_id

    else:
        print(response.text)
        return


def run():
    # Gets all tickets where a user has confirmed deletion with a 'DELETE ACCOUNT' response
    if not get_deletion_requests():
        return

    # Get the users active ADMIN token
    admin_token = input("Enter your active admin token: ")

    # For each email, get the agent ID and request if ready to delete, then send a confirmation to the user and close the ticket
    for email in emails_to_delete:
        print(f"Searching agent ID for: {email}")
        agent_id = get_agent_id(email, admin_token)

        while True:
            selection = input("Would you like to delete this user? y/n: ")

            if selection == 'y':
                delete_agent_id(agent_id, email, admin_token)
                break

            elif selection == 'n':
                break

            else:
                print("Enter a valid option: 'y'/'n'")
