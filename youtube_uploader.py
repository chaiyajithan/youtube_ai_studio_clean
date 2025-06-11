from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import os

# Scopes สำหรับ YouTube
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES
    )
    credentials = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=credentials)

def upload_video(file_path, title, description, tags=None, category="22", privacy="public"):
    youtube = authenticate_youtube()
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category,
        },
        "status": {
            "privacyStatus": privacy,
        },
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    upload_request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media,
    )
    response = upload_request.execute()
    return response.get("id")

