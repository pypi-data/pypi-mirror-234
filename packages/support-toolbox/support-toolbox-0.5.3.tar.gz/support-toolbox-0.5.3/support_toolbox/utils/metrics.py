from support_toolbox.utils.dataset import create_dataset
from support_toolbox.utils.org import onboard_org, authorize_access_to_org

BASEPLATFORM_DATASETS = [
    {
        "title": "baseplatformdata",
        "summary": "baseplatformdata is a collection of data.world platform-data tables. It is composed of four categories: audits, platform-analytics, platform-events, and platform-records. This dataset contains all the files found in the following datasets: platform-events, platform-records, platform-analytics and audits.",
        "visibility": "PRIVATE"
    },
    {
        "title": "platform-events",
        "summary": "Platform events logs by event type.",
        "visibility": "OPEN"
    },
    {
        "title": "platform-records",
        "summary": "Transactional records of platform resources (not including catalog metadata resources). Retention tables include deprovisioned or deleted resources.",
        "visibility": "OPEN"
    },
    {
        "title": "platform-analytics",
        "summary": "Fact and dimension tables designed for performant analytics and metrics queries.",
        "visibility": "OPEN"
    },
    {
        "title": "audits",
        "summary": "Audit events allow administrators to monitor the actions performed by all the users in the data.world application through the UI or while using API. The audit log reporting functionality enhances the accountability of actions in the application. Administrators can track the actions taken by users in the application and find the root cause of issues by identifying the resources on which the action was performed and who performed the action.",
        "visibility": "OPEN"
    }
]

DDW_METRICS_SUMMARY = """Metrics table- and column-level definitions here: [Documentation About Metrics](https://implementation.data.world/docs/about-metrics)

**Important caveat**: At the time that metrics updates are deployed, if any extraneous files have been added, they will be deleted by an automatic cleanup process. This dataset should not, therefore, be used for storage of any additional files.
### Usage and Governance Reporting 
* **Events** - _granular event data (30 or 90 day history)_ 
* **Membership** - _who is part of your account and when_ 
* **Resources** - _granular inventory of resources_
* **Tops** - _most active users, most frequent searches, etc._
* **Visits** - _how often is the tool used, by whom_"""


def deploy_metrics(admin_token, public_slug):
    # Ask user to select an option
    print("Before we continue, please select an option (1/2): ")
    print("1. Existing customer moving to a PI")
    print("2. New customer PI deployment")
    user_choice = input()

    # Set existing_customer based on user input
    if user_choice == "1":
        existing_customer = True
    elif user_choice == "2":
        existing_customer = False
    else:
        print("Invalid selection.")
        return

    metrics_deployment_choice = input("Start metrics deployment? (y/n): ")

    if metrics_deployment_choice.lower() == 'y':
        org_id = "data-catalog-team"
        org_display_name = "Data Catalog Team"

        standard_org_choice = input("Use the standard Data Catalog Team org (y/n): ")

        if standard_org_choice.lower() == 'n':
            org_id = input("Enter the org id: ")
            org_display_name = input("Enter the org display name: ")

        print(f"Onboarding {org_id}...")
        onboard_org(admin_token, org_id, org_display_name)

        print(f"Authorizing datadotworldsupport access to {org_id}...")
        authorize_access_to_org(admin_token, org_id, party='group:datadotworldsupport/members')

        if existing_customer:
            # Create the baseplatformdata dataset and subsequent four datasets that makeup baseplatformdata - this is default an "All Time" metrics deployment for Existing Customers
            for dataset in BASEPLATFORM_DATASETS:
                dataset_id = dataset['title']
                summary = dataset['summary']
                visibility = dataset['visibility']
                create_dataset(admin_token, org_id, dataset_id=dataset_id, visibility=visibility, summary=summary)

            # Create ddw-metrics-{public_slug} dataset - this is default an "All Time" metrics deployment for Existing Customers
            create_dataset(admin_token, org_id, dataset_id=f"ddw-metrics-{public_slug}", visibility="PRIVATE", summary=DDW_METRICS_SUMMARY)
            public_slug = public_slug + "_PI"

        else:
            all_time_metrics_choice = input("Is the customer paying for the 'All-time' metrics upgrade (y/n): ")

            if all_time_metrics_choice.lower() == 'y':
                # Create the baseplatformdata dataset and subsequent four datasets that makeup baseplatformdata - this handles when the NEW customer is paying for the "All Time" metrics deployment
                for dataset in BASEPLATFORM_DATASETS:
                    dataset_id = dataset['title']
                    summary = dataset['summary']
                    visibility = dataset['visibility']
                    create_dataset(admin_token, org_id, dataset_id=dataset_id, visibility=visibility, summary=summary)

                # Create ddw-metrics-{public_slug} dataset - this handles when the NEW customer is paying for the "All Time" metrics deployment
                create_dataset(admin_token, org_id, dataset_id=f"ddw-metrics-{public_slug}", visibility="PRIVATE", summary=DDW_METRICS_SUMMARY)
            else:
                # Create the baseplatformdata dataset and subsequent four datasets that makeup baseplatformdata - this handles the default LAST 90 DAYS metrics provided to NEW customers
                for dataset in BASEPLATFORM_DATASETS:
                    dataset_id = dataset['title'] + '-last-90-days'
                    summary = dataset['summary']
                    visibility = dataset['visibility']
                    create_dataset(admin_token, org_id, dataset_id=dataset_id, visibility=visibility, summary=summary)

                # Create ddw-metrics-{public_slug}-last-90-days dataset - this handles the default LAST 90 DAYS metrics provided to NEW customers
                create_dataset(admin_token, org_id, dataset_id=f"ddw-metrics-{public_slug}-last-90-days", visibility="PRIVATE", summary=DDW_METRICS_SUMMARY)

        return public_slug, org_id

    else:
        metrics_continue_choice = input("Do you want to continue without completing the metrics setup?\n"
                                        "We will skip creating the necessary org and datasets for metric deployment (y/n): ")

        if metrics_continue_choice.lower() == 'n':
            # Restart the metrics deployment process
            deploy_metrics(admin_token, public_slug)
        else:
            print("Continuing without metrics setup...")
