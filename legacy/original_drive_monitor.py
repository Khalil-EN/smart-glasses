from google.oauth2 import service_account
from googleapiclient.discovery import build
import subprocess
import time

def authenticate():
    creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=creds)
    return service

def list_files(folder_id, service):
    results = service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name, modifiedTime)").execute()
    files = results.get('files', [])
    return files

def check_for_updates(folder_id, service):
    last_modified_times = {}

    while True:
        files = list_files(folder_id, service)

        new_last_modified_times = {file['id']: file['modifiedTime'] for file in files}

        for file_id, modified_time in new_last_modified_times.items():
            if file_id in last_modified_times and modified_time != last_modified_times[file_id] and file_id='FILE_ID':
                with open('echange.txt', 'w') as file:
                    file.write('done')

        last_modified_times = new_last_modified_times 
        time.sleep(10)

service = authenticate()
folder_id = "FOLDER_ID"
check_for_updates(folder_id, service)
