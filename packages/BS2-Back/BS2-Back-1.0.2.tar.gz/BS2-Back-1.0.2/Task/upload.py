import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


# Path to the credentials JSON file for your service account
SERVICE_ACCOUNT_FILE = 'Api.json'

# Path to the folder on your local machine that you want to upload
LOCAL_FOLDER_PATH = 'Participant 12/'

# ID of the destination folder where you want to upload the folder
DESTINATION_FOLDER_ID = '1rUysUpmMihZTLPA8XL1INjRdA7bGbwZQ'

participant = 11

# Authenticate and authorize the service account
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
drive_service = build('drive', 'v3', credentials=creds)

# Function to create a folder in Google Drive
# Function to create a folder in Google Drive
def create_folder(folder_path, parent_id):
    folder_name = "Participant "+ str(participant)
    print(f'Folder name: {folder_name}')
    folder_metadata = {'name': folder_name, 'parents': [parent_id], 'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    print(f'Created folder {folder_name} with ID {folder.get("id")} in Google Drive')
    return folder.get('id')

# Function to upload a file to Google Drive
def upload_file(file_path, folder_id):
    file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'Uploaded file {file_metadata["name"]} with ID {file.get("id")} to Google Drive')

# Function to upload an entire folder to Google Drive as one folder, containing the individual files
def upload_folder(local_folder_path, parent_id):
    # Create a folder in Google Drive for the entire folder to be uploaded
    folder_name = os.path.basename(local_folder_path)
    folder_id = create_folder(folder_name, parent_id)
    # Upload each file in the folder to the created folder
    for file_name in os.listdir(local_folder_path):
        file_path = os.path.join(local_folder_path, file_name)
        if os.path.isfile(file_path):
            upload_file(file_path, folder_id)
        elif os.path.isdir(file_path):
            # Upload the subfolder recursively
            upload_folder(file_path, folder_id)

# Call the function to upload the entire folder to Google Drive as one folder, containing the individual files
upload_folder(LOCAL_FOLDER_PATH, DESTINATION_FOLDER_ID)
