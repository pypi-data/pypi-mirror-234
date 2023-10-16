from support_toolbox.utils.site import edit_saml, get_site_id
from support_toolbox.utils.helper import PRIVATE_API_URLS, SAMLMetadataParser


def run():
    api_url = PRIVATE_API_URLS['MT/PI']

    admin_token = input(f"Enter your active admin token for the site you are updating SAML for: ")

    while True:
        public_slug = input(f"Enter the public_slug for the PI you are updating SAML for: ")

        site_id, success = get_site_id(admin_token, public_slug, api_url)

        if success:
            break
        else:
            print(f"Unable to find the site_id for {public_slug}. Please try again.")

    default_org_list = input(f"Enter the default org_ids that users need access to (comma-separated): ")
    default_org_list = default_org_list.split(',')
    default_org_list = [default_org.strip() for default_org in default_org_list]

    print(f"Default org list: {default_org_list}")

    file_path = input(f'Enter the full path to the .xml SAML file on your computer: ')
    saml_parser = SAMLMetadataParser(file_path)
    entity_id = saml_parser.get_entity_id()
    sso_url = saml_parser.get_sso_url()
    x509_cert = saml_parser.get_x509_certificate()

    edit_saml(admin_token, entity_id, site_id, default_org_list, sso_url, x509_cert, api_url)

