import json
import requests
import csv
from support_toolbox.utils.helper import select_resource, select_api_url


# Clear User/Edit Layer on entire resource
def clear_entire_user_layer(api_token, org, iri, resource_type, customer_url):
    url = f"{customer_url}/metadata/{org}/resources/clear"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    clear_resource_data = {
        "resources": [iri],
        "resourceType": resource_type
    }

    body = json.dumps(clear_resource_data)
    response = requests.post(url, body, headers=header)

    # Verify the deletion
    if response.status_code == 200:
        print(f"Successfully cleared the User Layers for: {iri}")
    else:
        print(f"Unable to clear the User Layer for: {iri}\n{response.text}")


# Clear User/Edit Layer on specific properties
def clear_property_user_layer(api_token, org, iri, resource_type, properties, customer_url):
    url = f"{customer_url}/metadata/{org}/resources/properties/clear"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    clear_resource_data = {
        "resource": iri,
        "resourceType": resource_type,
        "properties": properties
    }

    body = json.dumps(clear_resource_data)
    response = requests.put(url, body, headers=header)

    # Verify the deletion
    if response.status_code == 200:
        print("Successfully cleared the User Layer for the following IRI's Properties:")
        print(iri)
        for p in properties:
            print(p)
    else:
        print(f"Unable to clear the User Layer for: {iri} | {response.text}")


# Function to select the clear method
def clear_user_layer(api_token, org, iris, resource_type, customer_url):
    clear_method = input("Enter `1` to clear the ENTIRE resource, or '2' to specify properties: ").strip().lower()

    if clear_method == "1":
        for r in iris:
            clear_entire_user_layer(api_token, org, r, resource_type, customer_url)

    elif clear_method == "2":
        properties_input = input("Enter the properties to clear (comma-separated or specify a CSV file path): ")

        if properties_input.endswith('.csv'):
            # User provided a CSV file path for properties, read and process it
            try:
                properties = process_csv_file(properties_input)
            except Exception as e:
                print(f"Error reading CSV file for properties: {str(e)}")
                return
        else:
            # User provided a comma-separated list, split and process it
            properties = [prop.strip() for prop in properties_input.split(',')]

        for r in iris:
            clear_property_user_layer(api_token, org, r, resource_type, properties, customer_url)
    else:
        print("Invalid choice. Please enter '1' or '2'.")


# Handle CSV input
def process_csv_file(file_path):
    iris = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            iris.extend(row)
    return iris


def run():
    api_url = select_api_url("public")
    api_token = input("Enter your API Token for the selected customer: ")
    org = input("Enter the org ID where the resources are located: ")

    # Allow the user to input multiple IRIs as a comma-separated list or specify a CSV file path
    iris_input = input("Enter the resource IRIs (comma-separated) or specify a CSV file path: ")

    if iris_input.endswith('.csv'):
        # User provided a CSV file path, read and process it
        try:
            iris = process_csv_file(iris_input)
        except Exception as e:
            print(f"Error reading CSV file: {str(e)}")
            return
    else:
        # User provided a comma-separated list, split and process it
        iris = [iri.strip() for iri in iris_input.split(',')]

    resource_type = select_resource()
    clear_user_layer(api_token, org, iris, resource_type, api_url)
