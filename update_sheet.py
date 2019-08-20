from __future__ import print_function
import pickle
import os.path
from httplib2 import Http
from urllib.error import HTTPError
from googleapiclient.discovery import build
from googleapiclient import errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    """ initial run will prompt for permissions from google drive
    -> this will generate pickle.
    returns service object
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    pickle_path = '/home/wayned/acquire/credentials/google_drive/token.pickle' 
    credentials_path = '/home/wayned/acquire/credentials/google_drive/credentials.json'
    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service


def update_file(service, file_id, new_mime_type,
                new_filename):
  """Update an existing file's metadata and content.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to update.
    new_mime_type: New MIME type for the file.
    new_filename: Filename of the new content to upload.
  Returns:
    Updated file metadata if successful, None otherwise.
  """
  try:
    # First retrieve the file from the API.
    file = service.files().get(fileId=file_id).execute()

    # File's new content.
    media_body = MediaFileUpload(
        new_filename, mimetype=new_mime_type, resumable=True)

    # Send the request to the API.
    updated_file = service.files().update(
        fileId=file_id,
        media_body=media_body).execute()
    return updated_file
  except errors.HttpError as error:
    print('An error occurred: %s' % error)
    return None

def uploadFile():
    """Uploads file to folder in drive specified by FOLDER ID,
    Must by modified for file meta data and mimetype
    """
    folder_id = '<FOLDER ID>'
    file_metadata = {
    'name': '<NAME>',
    'mimeType':'application/vnd.google-apps.spreadsheet',
    'parents': [folder_id]
    }
    media = MediaFileUpload('<NAME>',
                            mimetype='application/vnd.google-apps.spreadsheet',
                            resumable=True)
    file = drive_service.files().create(body=file_metadata,media_body=media,fields='id').execute()
    print ('File ID: %s ' % file.get('id'))

if __name__ == '__main__':
    service = main()
    update_file(service=service,
            file_id='14T3ni5gLjGg7_JMjnGZBRZ9GQ8ixV44k9Y4kLLktH9E',
            new_filename='/home/wayned/acquire/client_data/koho/weekly_reports/koho.csv',
            new_mime_type='application/vnd.google-apps.spreadsheet'
            )
