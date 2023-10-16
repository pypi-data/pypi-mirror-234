import os
import subprocess
import requests


def upload_file(api_token, org, dataset_id, file_path):
    # Construct the upload URL
    upload_file_url = f"https://api.data.world/v0/uploads/{org}/{dataset_id}/files"

    header = {
        'Authorization': f'Bearer {api_token}'
    }

    # Prepare the file data for multipart/form-data
    files = {'file': (os.path.basename(file_path), open(file_path, 'rb'))}

    # Use requests to upload the file as multipart/form-data
    response = requests.post(upload_file_url, headers=header, files=files)

    # Verify the upload
    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
        print("File uploaded successfully.")
    else:
        print(response.text)
        print("File upload failed.")


def copy_dwcc_file(version):
    # Construct the source path in the user's home directory
    source_path = os.path.expanduser("~/jar_files")

    # Check if the source directory exists, and create it if it doesn't
    if not os.path.exists(source_path):
        os.makedirs(source_path)

    # Define the target file name with the correct version
    target_file_name = f"dwcc{version}.jar"

    # Construct the Docker image tag
    docker_image_tag = f"datadotworld/dwcc:{version}"

    # Construct the Docker command without -it flags (non-interactive)
    docker_command = [
        "docker", "run", "--rm", "--entrypoint", "cp",
        f"--mount", f"type=bind,source={source_path},target=/dwcc-copy",
        docker_image_tag, "/app/dwcc.jar", f"/dwcc-copy/{target_file_name}"
    ]

    # Run the Docker command
    try:
        subprocess.run(docker_command, check=True)
        print(f"DWCC {version} file copied successfully as {target_file_name}.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def run():
    dwcc_version = input("Enter the latest DWCC version: ")
    api_token = input("Enter your API Token for the site you are uploading the latest dwcc.jar file to: ")
    org = input("Enter the org you are uploading to: ")
    dataset_id = input("Enter the project or dataset ID you are uploading to: ")

    # Construct the complete path to the copied DWCC file
    file_name = f"dwcc{dwcc_version}.jar"
    dwcc_file_path = os.path.expanduser(f"~/jar_files/{file_name}")

    # Check if the file exists before attempting to upload it
    if os.path.exists(dwcc_file_path):
        # Upload the file using the provided API token, org, dataset_id, and complete file path
        print(f"Uploading {file_name}, this may take a moment...")
        upload_file(api_token, org, dataset_id, dwcc_file_path)
    else:
        print(f"The {file_name} does not exist on your machine, one moment while I get that for you...")
        copy_dwcc_file(dwcc_version)
        print(f"Uploading {file_name}, this may take a moment...")
        upload_file(api_token, org, dataset_id, dwcc_file_path)
