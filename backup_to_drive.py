import os
import googleapiclient
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

file_path= "backup.sql.gz"
folder_id=os.environ.get('FOLDER_ID')

SCOPES = ['https://www.googleapis.com/auth/drive.file']

creds = Credentials(
  token=None, refresh_token=os.environ.get('REFRESH_TOKEN'),
  token_uri="https://oauth2.googleapis.com/token",
  client_id=os.environ.get('CLIENT_ID'),
  client_secret=os.environ.get('CLIENT_SECRET')
)


drive_service = build('drive', 'v3', credentials=creds)

file_metadata = {
  'name': os.path.basename(file_path),
  'parents': [folder_id]
}

media = googleapiclient.http.MediaFileUpload(file_path, resumable=True)
uploaded_file = drive_service.files().create(
    body=file_metadata,
    media_body=media,
    fields='id'
).execute()

print(f"File uploaded with ID: {uploaded_file['id']}")
