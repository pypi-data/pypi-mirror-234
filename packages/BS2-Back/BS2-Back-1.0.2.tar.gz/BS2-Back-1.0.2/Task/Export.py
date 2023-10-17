import os
import sys
from datetime import datetime
import subprocess
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import spwf

python_path = sys.executable
participant_number = spwf.participant_number
folder_name = f'Participant {participant_number}'
depfile = os.path.join(folder_name, f"Export Error.txt")
now = datetime.now()
date_time_string = now.strftime("%d-%m-%y")
outputtime = now.strftime("%H:%M:%S")

def upload():
    
    participant_number = spwf.participant_number
    folder_name = f'Participant {participant_number}'
    try:
        os.mkdir(folder_name)
        success = True
    except FileExistsError:
        success=False

    SERVICE_ACCOUNT_FILE = 'Api.json'

    LOCAL_FOLDER_PATH = folder_name

    #DESTINATION_FOLDER_ID = '1rUysUpmMihZTLPA8XL1INjRdA7bGbwZQ'
    DESTINATION_FOLDER_ID = '1bEpzafbGDmQWBaiFTnXb6Rxod3i9y7vG'

    # Authenticate and authorize the service account
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    credentials = service_account.Credentials.from_service_account_file(
    'Api.json',
    scopes=['https://www.googleapis.com/auth/drive']
)
    drive_service = build('drive', 'v3', credentials=creds)

    def create_folder(folder_path, parent_id):
        folder_name = os.path.basename(folder_path)
        #print(f'Folder name: {folder_name}')
        query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false and name='{folder_name}'"
        results = drive_service.files().list(q=query, fields='files(id)').execute().get('files', [])
        if len(results) > 0:
            folder_id = results[0]['id']
            return folder_id
        else:
            folder_metadata = {'name': folder_name, 'parents': [parent_id], 'mimeType': 'application/vnd.google-apps.folder'}
            folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
            return folder.get('id')

    def upload_file(file_path, folder_id):
        file_name = os.path.basename(file_path)
        query = f"'{folder_id}' in parents and mimeType!='application/vnd.google-apps.folder' and trashed=false and name='{file_name}'"
        results = drive_service.files().list(q=query, fields='files(id)').execute().get('files', [])
        if len(results) > 0:
            file_id = results[0]['id']
            file_metadata = {'name': file_name}
            media = MediaFileUpload(file_path, resumable=True)
            file = drive_service.files().update(fileId=file_id, body=file_metadata, media_body=media, fields='id').execute()
        else:
            file_metadata = {'name': file_name, 'parents': [folder_id]}
            media = MediaFileUpload(file_path, resumable=True)
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    def upload_folder(local_folder_path, parent_id): 
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

try:
    upload()
    print("Export complete")
except Exception as e:
    with open(depfile, mode='a+') as f:
        f.write(f'At {outputtime} an API error was experienced: \n\n ------------------------------------------------------ \n\n')
        f.write(str(e))
        print(e)
