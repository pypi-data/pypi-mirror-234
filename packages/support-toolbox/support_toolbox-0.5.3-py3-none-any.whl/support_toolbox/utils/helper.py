import xml.etree.ElementTree as ET
import os
import configparser

# Resource Types currently supported
ENTITIES = {
    'ANALYSIS': 'https://dwec.data.world/v0/Analysis',
    'BUSINESS_TERM': 'https://dwec.data.world/v0/BusinessTerm',
    'COLLECTION': 'https://dwec.data.world/v0/Catalog',
    'COLUMN': 'https://dwec.data.world/v0/DatabaseColumn',
    'DATA_TYPE': 'http://www.w3.org/ns/csvw#Datatype',
    'DATASET': 'https://dwec.data.world/v0/DwDataset',
    'TABLE': 'https://dwec.data.world/v0/DatabaseTable',
    'CUSTOM_TYPE': ''
}

PUBLIC_API_URLS = {
    "INDEED": "https://api.indeed.data.world/v0",
    "MCKINSEY": "https://api.mckinsey.data.world/v0",
    "MT/PI": "https://api.data.world/v0"
}

PRIVATE_API_URLS = {
    "INDEED": "https://cgtslzqhl5-admin.indeed.data.world/api/v0",
    "MCKINSEY": "https://tecsreqzb1-admin.mckinsey.data.world/api/v0",
    "MT/PI": "https://k2xz8y420efx4a3j.data.world/api/v0"
}

# List of tools and their corresponding token names
tools = {
    "delete_users": ["DWSUPPORT_API_TOKEN", "JIRA_API_TOKEN", "JIRA_USERNAME"],
    "deploy_service_accounts": ["CIRCLECI_API_TOKEN"],
    "deploy_pi": ["CIRCLECI_API_TOKEN"]
    # Add more tools and token names as needed here
}


def check_tokens(selected_tool):
    user_home = os.path.expanduser("~")
    config_file_path = os.path.join(user_home, ".tokens.ini")

    config = configparser.ConfigParser()

    if os.path.exists(config_file_path):
        config.read(config_file_path)

    if selected_tool not in config:
        config[selected_tool] = {}

    for token_name in tools.get(selected_tool, []):
        if token_name not in config[selected_tool]:
            token_value = input(f"Enter {token_name} for {selected_tool}: ")
            config[selected_tool][token_name] = token_value

    with open(config_file_path, "w") as configfile:
        config.write(configfile)


def select_api_url(api_type):
    if api_type == "private":
        api_urls = PRIVATE_API_URLS
    elif api_type == "public":
        api_urls = PUBLIC_API_URLS
    else:
        raise ValueError("Invalid API type. Use 'private' or 'public'")

    while True:
        for i, customer in enumerate(api_urls, start=1):
            print(f"{i}. {customer}")

        try:
            selection = int(input("Enter the number corresponding with the site your customer is in: "))
            if 1 <= selection <= len(api_urls):
                selected_customer = list(api_urls.keys())[selection - 1]
                return api_urls[selected_customer]
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def select_resource():
    while True:
        for i, entity in enumerate(ENTITIES, start=1):
            print(f"{i}. {entity}")

        try:
            selection = int(input(
                "Enter the number corresponding with the parent type of the resource: "))
            if 1 <= selection <= len(ENTITIES):
                if selection == 8:
                    resource_type = input(
                        "Enter the custom resource type IRI (ex. https://democorp.linked.data.world/d/ddw-catalogs/Sensor): ")
                    return resource_type
                return list(ENTITIES.values())[selection - 1]
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


class SAMLMetadataParser:
    def __init__(self, metadata_file_path):
        self.metadata_file_path = metadata_file_path
        self.root = self.parse_metadata_file()

    def parse_metadata_file(self):
        try:
            tree = ET.parse(self.metadata_file_path)
            return tree.getroot()
        except Exception as e:
            raise ValueError(f"Error parsing XML file: {str(e)}")

    def get_entity_id(self):
        entity_id = self.root.get('entityID')
        return entity_id

    def get_sso_url(self):
        sso_url_element = self.root.find('.//md:SingleSignOnService', namespaces={'md': 'urn:oasis:names:tc:SAML:2.0:metadata'})
        sso_url = sso_url_element.get('Location')
        return sso_url

    def get_x509_certificate(self):
        x509_cert_element = self.root.find('.//md:KeyDescriptor[@use="signing"]/ds:KeyInfo/ds:X509Data/ds:X509Certificate', namespaces={'md': 'urn:oasis:names:tc:SAML:2.0:metadata', 'ds': 'http://www.w3.org/2000/09/xmldsig#'})
        x509_cert_base64 = x509_cert_element.text

        # Add PEM delimiters
        pem_cert = f"-----BEGIN CERTIFICATE-----\n{x509_cert_base64}\n-----END CERTIFICATE-----"
        return pem_cert
