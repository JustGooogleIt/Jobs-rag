from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def download_files(folder_id, output_dir="downloads"):
  gauth = GoogleAuth()
  gauth.LocalWebserverAuth()
  drive = GoogleDrive(gauth)

  os.makedirs(output_dir, exist_ok=True)
  file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

  for file in file_list:
    print(f"Downloading {file['title']}")
    file.GetContentFile(os.path.join(output_dir, file['title']))

if __name__ == "__main__":
  from config import GOOGLE_DRIVE_FOLDER_ID
  download_files(GOOGLE_DRIVE_FOLDER_ID)