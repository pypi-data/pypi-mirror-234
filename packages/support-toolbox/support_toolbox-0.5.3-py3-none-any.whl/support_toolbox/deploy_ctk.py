import time
from support_toolbox.utils.org import onboard_org, authorize_access_to_org, deauthorize_access_to_org, validate_org_input
from support_toolbox.utils.user import get_agent_id

CTK_STACK = {
    'catalog-config': 'Catalog Config',
    'catalog-sources': 'Catalog Sources',
    'catalog-sandbox': 'Catalog Sandbox',
    'main': 'Main'
}

CTK_STACK_IMAGES = {
      'catalog-config': 'https://media.data.world/iSELaVlgTWeiy2bh2jhw_catalog-config.png',
      'catalog-sources': 'https://media.data.world/uDofsZwIR1SDUgUfEYp7_catalog-sources.png',
      'catalog-sandbox': 'https://media.data.world/Sue4Y8WVSrCqApwtZDvp_catalog-sandbox.png'
}


def sanitize_prefix(prefix):
    return prefix.lower().replace(' ', '-')


def deploy_ctk(admin_token, prefix=None):
    orgs_to_cleanup = []
    for org_id, org_display_name in CTK_STACK.items():
        avatar_url = '' if org_id == 'main' else CTK_STACK_IMAGES[org_id]
        if prefix:
            org_id = f"{prefix} {org_id}"
            org_id = org_id.replace(' ', '-').lower()
            org_display_name = f"{prefix} {org_display_name}"

        orgs_to_cleanup.append(org_id)
        onboard_org(admin_token, org_id, org_display_name, avatar_url)
        authorize_access_to_org(admin_token, org_id, party="group%3Adatadotworldsupport%2Fmembers")

    cleanup_ctk_deployment(admin_token, orgs_to_cleanup)


def cleanup_ctk_deployment(admin_token, orgs_to_cleanup):
    agent_id = get_agent_id(admin_token)

    for org_id in orgs_to_cleanup:
        # Platform lag is intense, use this to force a wait
        time.sleep(1)
        deauthorize_access_to_org(admin_token, agent_id, org_id)


def run():
    admin_token = input("Enter your active admin token for the site you are deploying CTK to: ")

    while True:
        selection = input("Does this CTK stack require an org prefix? (y/n): ")

        if selection == 'y':
            prefix = input("What would you like to call the Display Name for the org prefix? (CASE SENSITIVE): ")
            if validate_org_input(prefix):
                deploy_ctk(admin_token, prefix=prefix)
                break
            else:
                print('Invalid prefix name. Please try again.')

        else:
            main_display_name = input("What will the Display Name for the 'main' org be called? (CASE SENSITIVE): ")
            if validate_org_input(main_display_name):
                CTK_STACK['main'] = main_display_name
                deploy_ctk(admin_token)
                break
            else:
                print('Invalid organization name. Please try again.')
