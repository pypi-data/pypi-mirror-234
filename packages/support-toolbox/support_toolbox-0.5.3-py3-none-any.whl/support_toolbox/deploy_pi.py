import re
import os
import configparser
from support_toolbox.utils.helper import PRIVATE_API_URLS
from support_toolbox.utils.user import get_agent_id, add_support
from support_toolbox.deploy_browse_card import deploy_browse_card
from support_toolbox.deploy_integrations import deploy_integrations
from support_toolbox.utils.org import authorize_access_to_org, deauthorize_access_to_org, validate_org_input
from support_toolbox.deploy_ctk import deploy_ctk, CTK_STACK
from support_toolbox.utils.entitlements import update_org_entitlements, get_entitlements, get_default_values, update_default_plan, ORG_DEFAULT_ENTITLEMENTS, USER_DEFAULT_ENTITLEMENTS
from support_toolbox.utils.site import create_site, SAML_PLACEHOLDER, DEFAULT_ORGS
from support_toolbox.utils.service_account import create_service_account, create_env_variable, SERVICE_ACCOUNTS, CIRCLECI_PROJECTS
from support_toolbox.utils.metrics import deploy_metrics

# Get the path to the user's home directory
user_home = os.path.expanduser("~")

# Construct the full path to the configuration file
tokens_file_path = os.path.join(user_home, ".tokens.ini")

# Initialize the configparser and read the tokens configuration file
config = configparser.ConfigParser()
config.read(tokens_file_path)

# Read tokens/variables for the deploy_service_accounts tool
circleci_api_token = config['deploy_pi']['CIRCLECI_API_TOKEN']


def sanitize_public_slug(slug):
    # Convert to lowercase
    slug = slug.lower()

    # Remove spaces, symbols, and numbers
    slug = re.sub(r'[^a-z]+', '', slug)

    return slug


def config_site(admin_token):
    # Update the orgs that are created by default with the necessary Org Default Entitlements
    for org_id in DEFAULT_ORGS:
        source = get_entitlements(admin_token, org_id)
        order = 1
        for name, product_id in ORG_DEFAULT_ENTITLEMENTS.items():
            update_org_entitlements(admin_token, org_id, product_id, order, source, name)
            order += 1

    # Update Org Default Plan with the necessary ORG_DEFAULT_ENTITLEMENTS
    org_values = get_default_values(admin_token, "organization")
    org_agent_type = org_values['agent_type']
    org_offering_slug = org_values['offering_slug']
    org_offering_id = org_values['offering_id']
    org_product_ids = org_values['product_ids']

    # Update Product IDs with the ORG_DEFAULT_ENTITLEMENTS
    for entitlement in ORG_DEFAULT_ENTITLEMENTS.values():
        org_product_ids.append(entitlement)
    update_default_plan(admin_token, org_offering_id, org_agent_type, org_offering_slug, org_product_ids)

    # Update User Default Plan with the necessary USER_DEFAULT_ENTITLEMENTS
    user_values = get_default_values(admin_token, "user")
    user_agent_type = user_values['agent_type']
    user_offering_slug = user_values['offering_slug']
    user_offering_id = user_values['offering_id']
    user_product_ids = user_values['product_ids']

    # Update Product IDs with the USER_DEFAULT_ENTITLEMENTS
    for entitlement in USER_DEFAULT_ENTITLEMENTS.values():
        user_product_ids.append(entitlement)
    update_default_plan(admin_token, user_offering_id, user_agent_type, user_offering_slug, user_product_ids)

    # Authorize 'datadotworldsupport' access to 'ddw'
    authorize_access_to_org(admin_token, 'ddw', party="group:datadotworldsupport/members")


def deploy_service_accounts(api_token, site_slug, circleci_api_token):
    for i, sa in enumerate(SERVICE_ACCOUNTS):
        token = create_service_account(api_token, sa)

        # Configure parameters for CircleCI API
        circleci_project = CIRCLECI_PROJECTS[i]
        name = site_slug.upper() + "_API_TOKEN"

        create_env_variable(circleci_project, name, token, circleci_api_token=circleci_api_token)


def cleanup_site_creation(admin_token, metrics_org=''):
    agent_id = get_agent_id(admin_token)
    print(f"Cleaning up any resources {agent_id} is in...")

    for org_id in DEFAULT_ORGS:
        if org_id == 'datadotworldsupport':
            continue
        deauthorize_access_to_org(admin_token, agent_id, org_id)

    deauthorize_access_to_org(admin_token, agent_id, metrics_org)


def run():
    api_url = PRIVATE_API_URLS['MT/PI']

    while True:
        user_input = input("Enter the URL slug: ")
        public_slug = sanitize_public_slug(user_input)

        if not public_slug:
            print("Invalid slug. Please enter a valid URL slug.")
            continue

        preview_url = f"https://{public_slug}.app.data.world"
        selection = input(f"Here is a preview of the URL: {preview_url}\nDoes this look correct? (y/n): ")

        if selection == 'y':
            entity_id = SAML_PLACEHOLDER['entity_id']
            sso_url = SAML_PLACEHOLDER['sso_url']
            x509_cert = SAML_PLACEHOLDER['x509_cert']

            # Final verification before creating site
            print(f"\n{preview_url} will deploy with the following placeholder SAML values, be sure to update SAML once you have the SAML.xml file from the customer: ")
            print(f"SSO URL: {sso_url}")
            print(f"ENTITY ID: {entity_id}")
            print(f"x509 CERTIFICATE: {x509_cert}")

            #  Create site
            admin_token = input("Enter your active admin token for the community site to begin deployment: ")
            create_site(admin_token, entity_id, public_slug, sso_url, x509_cert, api_url)

            # Get the users active admin_token to complete the deployment using Private APIs
            admin_token = input(f"Enter your active admin token for the {public_slug} site: ")

            # Configure site with default entitlements, update org entitlements, update permissions
            config_site(admin_token)

            # Deploy CTK using the entered 'main' org as the Display Name
            while True:
                main_display_name = input("What will the Display Name for the 'main' org be called? (CASE SENSITIVE): ")
                if validate_org_input(main_display_name):
                    CTK_STACK['main'] = main_display_name
                    break
                else:
                    print('Invalid organization name. Please try again.')
            deploy_ctk(admin_token)

            # Deploy Metrics and return the altered public_slug used to create service accounts
            public_slug, metrics_org = deploy_metrics(admin_token, public_slug)

            print("Deploying browse card...")
            deploy_browse_card(admin_token, 'n')

            print("Deploying integrations...")
            deploy_integrations(admin_token, '1')

            print("Deploying service accounts...")
            deploy_service_accounts(admin_token, public_slug, circleci_api_token)

            cleanup_site_creation(admin_token, metrics_org)

            print("Adding the Support Team to the PI...")
            add_support(admin_token)
            break

        # URL Value denied
        elif selection == 'n':
            continue

        # URL Value invalid
        else:
            print("Enter a valid option: 'y'/'n'")
