import os
import json
from pathlib import Path
from typing import Optional

SCOPES = ['https://www.googleapis.com/auth/drive']
CURRENT_DIR = Path(__file__).resolve().parent
SERVICE_ACCOUNT_FILE = CURRENT_DIR / 'service_account.json'

# Google Drive Target Folder
DEFAULT_DRIVE_FOLDER_ID = '1Ftlwn2eiKTnLIHLIDpeX843Wz8byNaz7'

def get_drive_service():
    """Authenticate and return the Google Drive v3 API client."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    if not SERVICE_ACCOUNT_FILE.exists():
        raise FileNotFoundError(f"Service account file not found at: {SERVICE_ACCOUNT_FILE}")

    creds = service_account.Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_FILE), scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)

def upload_pdf_to_drive(local_pdf_path: str, file_name: Optional[str] = None, folder_id: Optional[str] = None) -> dict:
    """
    Uploads a local PDF to Google Drive, sets public view permissions,
    and returns both the webViewLink (for in-browser preview) and direct download link.
    """
    from googleapiclient.http import MediaFileUpload

    service = get_drive_service()
    path = Path(local_pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found at: {path}")

    target_folder = folder_id or DEFAULT_DRIVE_FOLDER_ID
    upload_name = file_name or path.name

    file_metadata = {
        'name': upload_name,
        'parents': [target_folder]
    }
    media = MediaFileUpload(str(path), mimetype='application/pdf', resumable=True)

    # 1. Create/Upload file
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, webViewLink, webContentLink'
    ).execute()

    file_id = file.get('id')

    # 2. Make file publicly viewable by anyone with the link
    try:
        service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
    except Exception as e:
        print(f"Warning setting permissions for {file_id}: {e}")

    # 3. Clean Google Drive links
    view_link = f"https://drive.google.com/file/d/{file_id}/view"
    download_link = f"https://drive.google.com/uc?export=download&id={file_id}"

    return {
        'status': 'success',
        'file_id': file_id,
        'name': upload_name,
        'view_url': view_link,
        'download_url': download_link
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        print(f"Testing upload of {test_file}...")
        res = upload_pdf_to_drive(test_file)
        print("Upload Result:", json.dumps(res, indent=2))
    else:
        print("Drive service ready. Run with: python backend/drive_service.py <path_to_pdf>")
